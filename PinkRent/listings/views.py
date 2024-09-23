from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render ,redirect
from . import models
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import ListingForm , ListingReviewForm, FeedbackForm, JoinWaitlistForm
from .models import Listing , FavoriteListing, ListingReview, Category, Tag, Brand
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count
from user_profiles.models import UserProfile, UserProfileReview, FavoriteUser
from django.template.loader import render_to_string

class JoinWaitlistView(generic.View):
    def get(self, request, *args, **kwargs):
        form = JoinWaitlistForm()
        return render(request, 'teaser.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = JoinWaitlistForm(request.POST)
        if form.is_valid():
            models.WaitlistEntry.objects.create(email=form.cleaned_data['email'])
            return redirect('waitlist/thank-you/')  # Replace 'success_page' with your success URL name
        return render(request, 'teaser.html', {'form': form})

def waitlist_thank_you_view(request):
    return render(request, 'waitlist_thank_you.html')

def main_page(request: HttpRequest) -> HttpResponse:
    listings = Listing.objects.filter(is_available=True)  # Filter only available listings
    context = {
        'listing_count': listings.count(),
        'users_count': models.get_user_model().objects.count(),
        'listings': listings,
    }
    if request.user.is_authenticated:
        user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__in=listings)
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids
    return render(request, 'main.html', context)

def shop_page(request):
    query = request.GET.get('q', '')
    city_query = request.GET.get('city', '')
    selected_tags = request.GET.getlist('tags')
    category_id = request.GET.get('category', 'all')
    parent_category_id = request.GET.get('parent_category', None)
    is_for_sale = request.GET.get('is_for_sale', '')
    sort_by_price_asc = request.GET.get('sort_by') == 'price_asc'
    sort_by_price_desc = request.GET.get('sort_by') == 'price_desc'
    brand_name = request.GET.get('brand', '')
    color_filter = request.GET.get('color', 'all')
    size_filter = request.GET.get('size', 'all')

    # Fetch parent categories (parent=None)
    parent_categories = Category.objects.filter(parent=None)
    
    # Initialize subcategories to None
    subcategories = None
    
    categories = Category.objects.all()
    listings = Listing.objects.filter(is_available=True)  # Filter only available listings

    # Apply filters
    if query:
        listings = listings.filter(name__icontains=query)
    
    if city_query:
        listings = listings.filter(owner__userprofile__city__icontains=city_query)

    if brand_name:
        listings = listings.filter(brand__name__icontains=brand_name)
        
    if is_for_sale == 'true':
        listings = listings.filter(is_for_sale=True)
    elif is_for_sale == 'false':
        listings = listings.filter(is_for_sale=False)

    if selected_tags:
        listings = listings.filter(tags__id__in=selected_tags).distinct()

    if category_id != 'all':
        listings = listings.filter(category__id=category_id)

    if category_id != 'all':
        listings = listings.filter(category__id=category_id)

    elif parent_category_id and parent_category_id != 'all':
        # Fetch listings based on selected parent category
        parent_category = get_object_or_404(Category, id=parent_category_id)
        subcategories = parent_category.subcategories.all()
        listings = listings.filter(category__parent_id=parent_category_id)
    
    if color_filter != 'all':
        listings = listings.filter(color=color_filter)

    if size_filter != 'all':
        listings = listings.filter(size=size_filter)

    # Sort by price per 4 days
    if sort_by_price_asc:
        listings = listings.order_by('price')
    elif sort_by_price_desc:
        listings = listings.order_by('-price')

    # Pagination
    paginator = Paginator(listings, 16)  # 4 listings per page
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    
    unique_colors = Listing.COLOR_CHOICES
    unique_sizes = (Listing.objects.values('size')
                .annotate(size_count=Count('size'))
                .order_by('size')
                .values_list('size', flat=True)
                .distinct())

    # Count active filters
    filter_counts = {
        'tags': len(selected_tags),
        'color': 1 if color_filter != 'all' else 0,
        'size': 1 if size_filter != 'all' else 0,
        'category': 1 if category_id != 'all' else 0,
        'parent_category': 1 if parent_category_id and parent_category_id != 'all' else 0,
        'brand': 1 if brand_name else 0,
        'is_for_sale': 1 if is_for_sale else 0,
        'sort_by': 1 if sort_by_price_asc or sort_by_price_desc else 0
    }
    total_filters = sum(filter_counts.values())

    context = {
        'listings': listings,
        'categories': categories,
        'parent_categories': parent_categories,
        'tags': Tag.objects.all(),
        'subcategories': subcategories,
        'brands': Brand.objects.all(),
        'colors': unique_colors,
        'sizes': unique_sizes,
        'filter_counts': filter_counts,
        'total_filters': total_filters,
        'query_params': request.GET.urlencode(),  # Provide cleaned URL parameters for pagination

    }

    if request.user.is_authenticated:
        user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__in=listings)
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids

    return render(request, 'shop.html', context)

def brand_search(request):
    query = request.GET.get('q', '')
    if query:
        brands = Brand.objects.filter(name__icontains=query).values('id', 'name')
    else:
        brands = Brand.objects.all().values('id', 'name')
    
    brand_list = list(brands)
    return JsonResponse(brand_list, safe=False)

def get_subcategories(request):
    parent_id = request.GET.get('parent_category')
    if parent_id:
        subcategories = Category.objects.filter(parent_id=parent_id)
    else:
        subcategories = Category.objects.filter(parent__isnull=False)

    subcategories_data = [{'id': subcat.id, 'name': subcat.name} for subcat in subcategories]
    return JsonResponse({'subcategories': subcategories_data})

def category_page(request, category_slug, parent_slug=None):
    # Fetch category based on parent_slug if provided
    if parent_slug:
        parent_category = get_object_or_404(Category, slug=parent_slug, parent=None)
        category = get_object_or_404(Category, slug=category_slug, parent=parent_category)
    else:
        category = get_object_or_404(Category, slug=category_slug, parent=None)
    listings = Listing.objects.filter(category=category)
    
    # Pagination
    paginator = Paginator(listings, 8)  # 4 listings per page
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'listings': listings,
    }

    if request.user.is_authenticated:
        user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__in=listings)
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids
    
    return render(request, 'category_page.html', context)


def how_it_works(request):
    return render(request, 'pages/how_it_works.html')

def terms_and_conditions(request):
    return render(request, 'pages/terms_and_conditions.html')

def best_practices_lending(request):
    return render(request, 'pages/how_to_lend.html')

def listing_upload_guidelines(request):
    return render(request, 'pages/listing_upload_guidelines.html')

def fashion_rental_tips(request):
    return render(request, 'pages/how_to_rent.html')

def about_us(request):
    return render(request, 'pages/about_us.html')

def platform_rules(request):
    return render(request, 'pages/platform_rules.html')

def listing_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Listing.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    next = request.path + '?' + '&'.join([f"{key}={value}" for key, value in request.GET.items()])
    context = {
        'listing_list': queryset.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
        'next': next,
    }
    return render(request, 'listings/listing_list.html', context)

def listing_detail(request: HttpRequest, pk:int) -> HttpResponse:
    listing = get_object_or_404(Listing, pk=pk)
    owner = listing.owner  # Assumes `owner` is a ForeignKey to the user in the Listing model
    owner_profile = get_object_or_404(UserProfile, user=owner)
    context = {
        'listing': listing,
        'owner_profile': owner_profile,
    }
    if request.user.is_authenticated:
        context['user_favorites'] = FavoriteListing.objects.filter(user=request.user, favorite_listing=listing)
    listing_reviews = ListingReview.objects.filter(listing=listing)

    # Calculate average rating
    average_rating = listing_reviews.aggregate(Avg('rate'))['rate__avg']
    context['average_rating'] = average_rating if average_rating is not None else 0

    context['listing_reviews'] = listing_reviews

    profile_reviews = UserProfileReview.objects.filter(profile=owner_profile)

    # Calculate average rating
    profile_average_rating = profile_reviews.aggregate(Avg('rate'))['rate__avg']
    context['profile_average_rating'] = profile_average_rating if profile_average_rating is not None else 0

    context['profile_reviews'] = profile_reviews

    return render(request, 'listings/listing_details.html', context)

def listing_available(request: HttpRequest, pk:int) -> HttpResponse:
    listing = get_object_or_404(models.Listing, pk=pk)
    if request.user in [listing.owner]:
        listing.is_available = not listing.is_available
        listing.save()
        messages.success(request, "{} {} {} {}".format(
            _('listing').capitalize(),
            listing.name,
            _('marked as'),
            _('available') if listing.is_available else _('unavailable'),
        ))
    else:
        messages.error(request, "{}: {}".format(_("permission error").title(), _("you must be the owner of listing"),))
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect(listing_list)


def my_listings(request):
    user_listings = Listing.objects.filter(owner=request.user)
    return render(request, 'listings/my_listings.html', {'user_listings': user_listings})

    
class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Listing
    template_name = 'listings/listing_create.html'
    form_class = ListingForm

    def get_success_url(self) -> str:
        messages.success(self.request, _('listing created successfully').capitalize())
        return reverse('listings:listing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(parent=None)
        return context
    
class ListingUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Listing
    template_name = 'listings/listing_update.html'
    form_class = ListingForm

    def get_success_url(self) -> str:
        messages.success(self.request, _('listing updated successfully').capitalize())
        return reverse('user_detail_current')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = models.Category.objects.filter(parent__isnull=True)
        context['favorite_listing_ids'] = self.request.user.favorite_listings.values_list('id', flat=True)
        return context
    
class ListingDeleteView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.DeleteView
    ):
    model = models.Listing
    template_name = 'listings/listing_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, _('listing deleted successfully').capitalize())
        return reverse('user_detail_current')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user

def add_favorite_listing(request, pk):
    # Get the listing object to be added as a favorite
    favorite_listing = get_object_or_404(Listing, pk=pk)

    # Check if the favorite already exists for the current user
    existing_favorite = FavoriteListing.objects.filter(user=request.user, favorite_listing=favorite_listing).exists()
    if not existing_favorite:
        # Create a new favorite entry for the current user
        FavoriteListing.objects.create(user=request.user, favorite_listing=favorite_listing)
        messages.success(request, 'Listing added as favorite successfully.')
    else:
        messages.info(request, 'Listing is already a favorite.')

    # Redirect back to the page where the form was submitted
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect('listings:my_favorites')

@login_required
def my_favorites(request):
    listing_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__is_available=True)
    context = {
        'listing_favorites': listing_favorites,
    }
    return render(request, 'favorite/my_favorite_listings.html', context)

@login_required
def my_favorite_users(request):
    favorite_users = FavoriteUser.objects.filter(user=request.user)
    return render(request, 'favorite/my_favorite_users.html', {'favorite_users': favorite_users})

def remove_favorite_listing(request, pk):
    if request.method == 'POST':
        listing_to_remove = get_object_or_404(Listing, pk=pk)
        favorite_to_remove = get_object_or_404(FavoriteListing, user=request.user, favorite_listing=listing_to_remove)
        favorite_to_remove.delete()
        messages.success(request, 'Listing removed from favorites successfully.')
        # Optionally, you can redirect the user to a different page after removal
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect('listings:my_favorites')
    else:
        # Handle GET requests or other cases as needed
        return HttpResponse('Method not allowed', status=405)

def create_listing_review(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        form = ListingReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.listing = listing  # Assign the listing to the review
            review.save()
            messages.success(request, 'Listing review created successfully!')
            return redirect(reverse('listings:listing_review_success'))  # Redirect using reverse
    else:
        form = ListingReviewForm()
    
    return render(request, 'reviews/create_listing_review.html', {'form': form, 'listing': listing})

def listing_review_success(request):
    return render(request, 'reviews/listing_review_success.html')

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            return redirect('listings:feedback_thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback.html', {'form': form})

def feedback_thank_you_view(request):
    return render(request, 'feedback/feedback_thank_you.html')
