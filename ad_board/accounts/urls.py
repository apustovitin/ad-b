from django.urls import path
from .views import UserProfile, EditProfile

urlpatterns = [
    path('<str:username>/', UserProfile.as_view(), name='profile'),
    path('<str:username>/edit', EditProfile.as_view(), name='edit_profile'),
]