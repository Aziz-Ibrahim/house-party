from django.shortcuts import redirect, render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post

from .utils import (
    get_user_tokens,
    update_or_create_user_tokens
)

class AuthURL(APIView):
    """
    View to handle authentication-related requests.
    """
    def get(self, request, format=None):
        """
        Handle GET requests for authentication.
        """
        scopes = (
            'user-read-playback-state user-modify-playback-state'
            'user-read-currently-playing'
            )
        url = Request(
            'GET',
            'https://accounts.spotify.com/authorize',
            params={
                'scope': scopes,
                'response_type': 'code',
                'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
                'client_id': settings.SPOTIFY_CLIENT_ID,
            }
        ).prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    """
    Handle the Spotify callback after authentication.
    """
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
    ).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key,
        access_token,
        token_type,
        expires_in,
        refresh_token
    )

    return redirect('frontend:')