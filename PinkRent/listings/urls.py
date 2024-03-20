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
]

