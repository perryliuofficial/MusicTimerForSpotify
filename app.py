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
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from json.decoder import JSONDecodeError
import pandas as pd
import pprint
from time import sleep

# These are stored within .env, which is gitignored.
SPOTIPY_CLIENT_ID=config('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=config('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI=config('REDIRECT_URI')
# -----------------------------------------------
# The contents of the .env file should look like this:
# CLIENT_ID=000000000000000000000000
# CLIENT_SECRET=000000000000000000000000
# REDIRECT_URI='http://google.com'