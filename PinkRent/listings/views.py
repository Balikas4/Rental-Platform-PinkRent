from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render ,redirect
from . import models
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import ListingForm , ListingReviewForm
from .models import Listing , FavoriteListing, ListingReview, Category, Tag
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from user_profiles.models import UserProfile

def main_page(request: HttpRequest) -> HttpResponse:
    listings = Listing.objects.all()
    context = {
        'listing_count': models.Listing.objects.count(),
        'users_count': models.get_user_model().objects.count(),
        'listings': models.Listing.objects.all(),
    }
    if request.user.is_authenticated:
        user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__in=listings)
        # Create a set of favorite listing ids for easier lookup
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids
    return render(request, 'main.html', context)

def shop_page(request):
    query = request.GET.get('q', '')
    selected_tags = request.GET.getlist('tags')
    category_id = request.GET.get('category', 'all')
    search_query = request.GET.get('search')

    listings = Listing.objects.all()

    # Filter by name query
    if query:
        listings = listings.filter(name__icontains=query)

    # Filter by selected tags
    if selected_tags:
        listings = listings.filter(tags__id__in=selected_tags).distinct()

    # Filter by category
    if category_id != 'all':
        listings = listings.filter(category__id=category_id)

    # Filter by search query
    if search_query:
        listings = listings.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(listings, 4)  # 4 listings per page
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {
        'listings': listings,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }

    if request.user.is_authenticated:
        user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing__in=listings)
        # Create a set of favorite listing ids for easier lookup
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids

    return render(request, 'shop.html', context)

def category_page(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    listings = Listing.objects.filter(category=category)
    
    # Pagination
    paginator = Paginator(listings, 4)  # 4 listings per page
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
        # Create a set of favorite listing ids for easier lookup
        favorite_listing_ids = set(user_favorites.values_list('favorite_listing__id', flat=True))
        context['favorite_listing_ids'] = favorite_listing_ids
    
    return render(request, 'category_page.html', context)

def how_it_works(request):
    return render(request, 'how-it-works.html')

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
    context = {
        'listing': listing,
    }
    if request.user.is_authenticated:
        context['user_favorites'] = FavoriteListing.objects.filter(user=request.user, favorite_listing=listing)
    reviews = ListingReview.objects.filter(listing=listing)

    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rate'))['rate__avg']
    context['average_rating'] = average_rating if average_rating is not None else 0

    context['reviews'] = reviews
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
        return reverse('listings:my_listings')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
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
        return reverse('listings:my_listings')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user
    
class ListingDeleteView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.DeleteView
    ):
    model = models.Listing
    template_name = 'listings/listing_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, _('listing deleted successfully').capitalize())
        return reverse('listings:my_listings')

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

def my_favorites(request):
    listing_favorites = FavoriteListing.objects.filter(user=request.user)
    return render(request, 'favorite/my_favorite_listings.html', {'listing_favorites': listing_favorites})

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