from django.urls import path
from .views import *

app_name = 'offers'

urlpatterns = [
    path('send/', send_offer, name='send_offer'),
    path('send/<int:listing_id>/', send_offer, name='send_offer_with_listing'),
    path('sent/', offer_sent, name='offer_sent'),
    path('my_offers/', my_offers, name='my_offers'),
    path('accept_offer/<int:pk>/', accept_offer, name='accept_offer'),
    path('reject_offer/<int:pk>/', reject_offer, name='reject_offer'),
    path('offer/<int:pk>/', offer_details, name='offer_details'),
]
