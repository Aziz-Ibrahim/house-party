from django.urls import path

from .views import *


urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),  # Endpoint for authentication
    path('redirect', spotify_callback),  # Callback endpoint
    path('is-authenticated', IsAuthenticated.as_view()),  # Check if user is authenticated
    path('current-song', CurrentSong.as_view()),  # Get current song
    path('pause', PauseSong.as_view()),  # Pause the current song
    path('play', PlaySong.as_view()),  # Play the current song
]