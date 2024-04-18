from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/available/', views.listing_available, name='listing_available'),
    path('listings/create/', views.ListingCreateView.as_view(), name='listing_create'),
    path('listing/<int:pk>/edit/', views.ListingUpdateView.as_view(), name='listing_update'),
    path('listing/<int:pk>/delete/', views.ListingDeleteView.as_view(), name='listing_delete'),
    path('my_listings/', views.my_listings, name="my_listings"),
    path('shop/', views.shop_page, name='shop_page'),
    # URLs for adding and removing favorite listings
    path('listing/<int:pk>/favorite/', views.add_favorite_listing, name='add_favorite_listing'),
    path('listing/<int:pk>/unfavorite/', views.remove_favorite_listing, name='remove_favorite_listing'),
    path('listing/my_favorites/', views.my_favorites, name="my_favorites"),
    # URLs for listing filtering
    path('<slug:category_slug>/', views.category_page, name='category_page'),
]
