import os
from decouple import config
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid 
import requests
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# These are stored within .env, which is gitignored.
CLIENT_ID=config('CLIENT_ID')
CLIENT_SECRET=config('CLIENT_SECRET')
#SPOTIPY_REDIRECT_URI=config('SPOTIPY_REDIRECT_URI')
# -----------------------------------------------
# The contents of the .env file should look like this
# SPOTIPY_CLIENT_ID=000000000000000000000000
# SPOTIPY_CLIENT_SECRET=000000000000000000000000
# SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080'


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

r = r.json()
r