from flask import Flask, render_template, request, Response, redirect, url_for, flash
from app import app, sp
from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.forms import InputForm

app.config['SECRET_KEY']=config('FLASK_WTF_KEY') #Flask WTF key

################################################################################################################################## 
################################################################################################################################## 
@app.route('/', methods=['POST', 'GET'])
def index():
    stage = 0
    return render_template('index.html', stage=stage)
################################################################################################################################## 
##################################################################################################################################  
@app.route("/timer/", methods=['POST', 'GET'])
def timer():
    stage = 1
    CLIENT_ID=config('CLIENT_ID')
    CLIENT_SECRET=config('CLIENT_SECRET')
    REDIRECT_URI=config('REDIRECT_URI')

    scope = "user-library-read playlist-read-private playlist-modify-private user-modify-playback-state"
    global sp 
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
    )

    #################################################################
    # Get user ID
    results = sp.current_user()
    user_id = results["id"]

    #################################################################
    # check if Timer playlist exists, if not create it. Also get the playlist id
    results = sp.current_user_playlists()
    playlist_items = results["items"]

    timerPlaylistExists = False
    timerPlaylistId: str

    for item in playlist_items:
        name = item["name"]
        if name == "Spotify Music Timer":
            timerPlaylistExists = True
            timerPlaylistId = item["id"]
            break

    if not timerPlaylistExists:
        response = sp.user_playlist_create(
            user=user_id,
            name="Spotify Music Timer",
            public=False,
            collaborative=False,
            description="Spotify Music Timer",
        )
        timerPlaylistId = response["id"]

    #################################################################
    # clear the playlist to ensure only the songs we want to play are there
    def clearPlaylist():
        current_timer_playlist_songs = sp.playlist_items(playlist_id=timerPlaylistId, fields="items(track(id))")
        trackIds = list()
        for track in current_timer_playlist_songs["items"]:
            trackIds.append(track["track"]["id"])
        sp.playlist_remove_all_occurrences_of_items(playlist_id=timerPlaylistId, items=trackIds)

    clearPlaylist()

    form = InputForm()
    if request.method == 'POST':
        timer = form.timer.data
        return redirect(url_for('playlist', stage=stage, title='Music Timer for Spotify', user_id=user_id, timer=timer))
    else :
        return render_template('index.html', stage=stage, title='Music Timer for Spotify', user_id=user_id, form=form)

################################################################################################################################## 
################################################################################################################################## 
@app.route('/playlist',methods=['POST', 'GET'])
def playlist():
    stage = 3

    timer = request.form.get('timer')
    # print(timer)
    
    #################################################################
    # Select Playlist
    global sp
    results = sp.current_user_playlists()

    # print ("SELECT PLAYLIST")
    # print ("---------------")
    # for count, playlist_results in enumerate(results['items']):
    #     print (str(count) +": "+ playlist_results['name'])

    # playlist_selection = int(input("Enter playlist number: "))
    # playlist_id = results['items'][playlist_selection]['id']

    return render_template('playlist.html', title='Music Timer for Spotify', stage=stage, timer=timer, results=results)