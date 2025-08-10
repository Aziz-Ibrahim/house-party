from django.urls import path

from .views import AuthURL, spotify_callback, IsAuthenticated


urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),  # Endpoint for authentication
    path('redirect', spotify_callback),  # Callback endpoint
    path('is-authenticated', IsAuthenticated.as_view()),  # Check if user is authenticated
]