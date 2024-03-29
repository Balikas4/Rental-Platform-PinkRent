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
from .forms import ListingForm
from .models import Listing , FavoriteListing

def main_page(request: HttpRequest) -> HttpResponse:
    context = {
        'listing_count': models.Listing.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'main.html', context)

def shop_page(request: HttpRequest) -> HttpResponse:
    context = {
        'listings' : Listing.objects.all(),
    }
    return render(request, 'shop.html', context)

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
    user_favorites = FavoriteListing.objects.filter(user=request.user, favorite_listing=listing)
    return render(request, 'listings/listing_details.html', {
        'listing': get_object_or_404(models.Listing, pk=pk),
        'user_favorites': user_favorites,
        'listing': listing,
    })

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