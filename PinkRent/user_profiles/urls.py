from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('detail/', views.user_detail, name='user_detail_current'),
    path('detail/<str:username>/', views.user_detail, name='user_detail'),
    path('user_update/', views.user_update, name='user_update'),
    path('favorite/<int:user_id>/', views.add_favorite_user, name='favorite_user'),
    path('remove_favorite/<int:user_id>/', views.remove_favorite_user, name='remove_favorite'),
    path('my_favorites/', views.my_favorite_users, name='my_favorite_users'),
    path('profile/<int:profile_id>/create_profile_review/', views.create_profile_review, name='create_profile_review'),
    path('profile_review_success/', views.profile_review_success, name='profile_review_success'),
]
