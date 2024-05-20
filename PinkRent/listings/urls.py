from django.urls import path
from . import views
from django.contrib import admin

app_name = 'listings'

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.main_page, name='main_page'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/available/', views.listing_available, name='listing_available'),
    path('listings/create/', views.ListingCreateView.as_view(), name='listing_create'),
    path('listing/<int:pk>/edit/', views.ListingUpdateView.as_view(), name='listing_update'),
    path('listing/<int:pk>/delete/', views.ListingDeleteView.as_view(), name='listing_delete'),
    path('my-listings/', views.my_listings, name="my_listings"),
    path('shop/', views.shop_page, name='shop_page'),
    path('how-it-works/', views.how_it_works, name='how-it-works'),
    # URLs for adding and removing favorite listings
    path('listing/<int:pk>/favorite/', views.add_favorite_listing, name='add_favorite_listing'),
    path('listing/<int:pk>/unfavorite/', views.remove_favorite_listing, name='remove_favorite_listing'),
    path('listing/my_favorites/', views.my_favorites, name="my_favorites"),
    path('listing/<int:listing_id>/create-listing-review/', views.create_listing_review, name='create_listing_review'),
    path('listing-review-success/', views.listing_review_success, name='listing_review_success'),
    # URLs for listing filtering
    path('<slug:parent_slug>/<slug:category_slug>/', views.category_page, name='category_page'),
    path('<slug:category_slug>/', views.category_page, name='category_page'),
]
