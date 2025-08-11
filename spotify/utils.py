from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from requests import post, put, get

from .models import SpotifyToken


BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    """
    Retrieve the Spotify tokens for a user based on their session ID.
    Args:
        session_id (str): The session ID of the user.
    Returns:
        SpotifyToken: The user's Spotify token object if it exists,
        otherwise None.
    """
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    print(user_tokens)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token
    ):
    """
    Update or create a Spotify token for a user.
    Args:
        session_id (str): The session ID of the user.
        access_token (str): The Spotify access token.
        token_type (str): The type of the token.
        expires_in (int): The expiration time of the token in seconds.
        refresh_token (str): The Spotify refresh token.
    """
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(
            update_fields=[
                'access_token',
                'refresh_token',
                'expires_in',
                'token_type'
            ]
        )
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in
        )
        tokens.save()


def is_spotify_authenticated(session_id):
    """
    Check if the user is authenticated with Spotify.
    Args:
        session_id (str): The session ID of the user.
    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    """
    Refresh the Spotify access token for a user.
    Args:
        session_id (str): The session ID of the user.
    """
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET
        }
    ).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(
        session_id,
        access_token,
        token_type,
        expires_in,
        refresh_token
    )


def execute_spotify_api_request(
        session_id,
        endpoint,
        post_=False,
        put_=False
    ):
    """
    Execute a request to the Spotify API.
    Args:
        session_id (str): The session ID of the user.
        endpoint (str): The API endpoint to call.
        post_ (bool): Whether to use POST method.
        put_ (bool): Whether to use PUT method.
        put_data (dict): Data to send with PUT request.
    Returns:
        dict: The JSON response from the API.
    """
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + tokens.access_token
    }
    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Invalid response'}