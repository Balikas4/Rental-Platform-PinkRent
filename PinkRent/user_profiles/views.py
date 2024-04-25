from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile , FavoriteUser, UserProfileReview
from .forms import ProfileReviewForm
from listings.models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.db.models import Avg


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thank you! You can log in now with your credentials."))
            return redirect("login")
    else:
        form = forms.CreateUserForm()
    return render(request, 'user_profile/signup.html', {
        'form': form,
    })

User = get_user_model()

@login_required
def user_detail(request: HttpRequest, username: str | None = None)  -> HttpResponse:
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    unavailable_listings_count = user.listings.filter(is_available=False).count()
    user_favorites = FavoriteUser.objects.filter(user=request.user, favorite_user=user)
    current_profile = get_object_or_404(UserProfile, user=user)
    profile_listings = Listing.objects.filter(owner=user)
    # Pagination
    paginator = Paginator(profile_listings, 3)  # 3 listings per page
    page = request.GET.get('page')
    try:
        profile_listings = paginator.page(page)
    except PageNotAnInteger:
        profile_listings = paginator.page(1)
    except EmptyPage:
        profile_listings = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'unavailable_listings_count': unavailable_listings_count,
        'user_favorites': user_favorites,
        'current_profile': current_profile,
        'profile_listings': profile_listings,
    }
    reviews = UserProfileReview.objects.filter(profile=current_profile)

    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rate'))['rate__avg']
    context['average_rating'] = average_rating if average_rating is not None else 0

    context['reviews'] = reviews
    return render(request, 'user_profile/user_detail.html', context)

@login_required
def user_update(request: HttpRequest) -> HttpResponse:
    try:
        # Try to get the user's profile
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        # If the profile doesn't exist, create a new one
        profile = UserProfile(user=request.user)
        profile.save()

    if request.method == "POST":
        form_user = forms.UserForm(request.POST, instance=request.user)
        form_profile = forms.UserProfileForm(request.POST, request.FILES, instance=profile)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            messages.success(request, _("Profile edited successfully").capitalize())
            return redirect('user_detail_current')

    else:
        form_user = forms.UserForm(instance=request.user)
        form_profile = forms.UserProfileForm(instance=profile)

    return render(request, 'user_profile/user_update.html', {
        'form_user': form_user,
        'form_profile': form_profile,
    })

@login_required
def add_favorite_user(request, user_id):
    # Get the user object to be added as a favorite
    favorite_user = get_object_or_404(get_user_model(), pk=user_id)

    # Check if the favorite already exists for the current user
    existing_favorite = FavoriteUser.objects.filter(user=request.user, favorite_user=favorite_user).exists()
    if not existing_favorite:
        # Create a new favorite entry for the current user
        FavoriteUser.objects.create(user=request.user, favorite_user=favorite_user)
        messages.success(request, 'User added as favorite successfully.')
    else:
        messages.info(request, 'User is already a favorite.')

    # Redirect back to the page where the form was submitted
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect('my_favorite_users')

@login_required
def my_favorite_users(request):
    user_favorites = FavoriteUser.objects.filter(user=request.user)
    return render(request, 'favorite/my_favorite_users.html', {'user_favorites': user_favorites})

@login_required
def remove_favorite_user(request, user_id):
    if request.method == 'POST':
        user_to_remove = get_object_or_404(get_user_model(), id=user_id)
        favorite_to_remove = get_object_or_404(FavoriteUser, user=request.user, favorite_user=user_to_remove)
        favorite_to_remove.delete()
        messages.success(request, 'User removed from favorites successfully.')
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect('my_favorite_users')
    else:
        # Handle GET requests or other cases as needed
        return HttpResponse('Method not allowed', status=405)

def create_profile_review(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    
    if request.method == 'POST':
        form = ProfileReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.profile = profile  # Assign the profile to the review
            review.save()
            messages.success(request, 'Profile review created successfully!')
            return redirect(reverse('profile_review_success'))  # Redirect using reverse
    else:
        form = ProfileReviewForm()
    
    return render(request, 'reviews/create_profile_review.html', {'form': form, 'profile': profile})

def profile_review_success(request):
    return render(request, 'reviews/profile_review_success.html')