# messenger/urls.py
from django.urls import path
from .views import conversation_list, conversation_detail, start_conversation

app_name = 'messenger'  # Set the namespace for this app

urlpatterns = [
    path('', conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('conversation/create/<int:listing_id>/', start_conversation, name='create_conversation'),
]
