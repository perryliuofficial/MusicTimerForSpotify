import os
import sys
import json
import webbrowser
from decouple import config
from flask import Flask, session, request, redirect
from flask_session import Session
from speech_recognition import Microphone, Recognizer, UnknownValueError
import spotipy
import spotipy.util as util
import uuid 
import requests
import base64
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from json.decoder import JSONDecodeError
import pandas as pd
import pprint
from time import sleep

# These are stored within .env, which is gitignored.
CLIENT_ID=config('CLIENT_ID')
CLIENT_SECRET=config('CLIENT_SECRET')
REDIRECT_URI=config('REDIRECT_URI')
# -----------------------------------------------
# The contents of the .env file should look like this:
# CLIENT_ID=000000000000000000000000
# CLIENT_SECRET=000000000000000000000000
# REDIRECT_URI='http://google.com'

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{CLIENT_ID}:{CLIENT_SECRET}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

# Step 2 - Get Current User's Playlists
# playLists = f"https://api.spotify.com/v1/me/playlists"
# headers = {
#     "Authorization": "Bearer " + token
# }

# res = requests.get(
#     url=playLists,
#     headers=headers)

# print(json.dumps(res.json(), indent=2))

# Step X - Use Access Token to call playlist endpoint
playlistId = "37i9dQZF1DWZeKCadgRdKQ"
playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
headers = {
    "Authorization": "Bearer " + token
}

res = requests.get(url=playlistUrl, headers=headers)

print(json.dumps(res.json(), indent=2))