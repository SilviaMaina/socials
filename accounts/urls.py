from django.urls import path, include
from .views import index, register, login, my_profile_view, update_profile, follow_user, unfollow_user, list_followers, search_users

urlpatterns = [
    path('', index, name='index'),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),

    path('api/profile/', my_profile_view, name='my-profile'),
    path('api/profile/update', update_profile, name='update-profile'),

    path('api/users/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('api/users/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('api/users/<int:user_id>/followers/', list_followers, name='list_followers'),

    path('api/search/users/', search_users, name='search_users'),

]