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
REDIRECT_URI=config('REDIRECT_URI')
# -----------------------------------------------
# The contents of the .env file should look like this:
# CLIENT_ID=000000000000000000000000
# CLIENT_SECRET=000000000000000000000000
# REDIRECT_URI='http://google.com'
