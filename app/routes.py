from flask import Flask, render_template, request, Response, redirect, url_for, flash
from app import app, sp, playlist_id, timer, timerPlaylistId, user_id
from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.forms import InputForm, PlaylistForm
import json
import time

app.config['SECRET_KEY']=config('FLASK_WTF_KEY') #Flask WTF key

################################################################################################################################## 
################################################################################################################################## 
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
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
    global user_id
    user_id = results["id"]

    #################################################################
    # check if Timer playlist exists, if not create it. Also get the playlist id
    results = sp.current_user_playlists()
    playlist_items = results["items"]

    timerPlaylistExists = False
    global timerPlaylistId

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
        return redirect(url_for('playlist',stage=stage,form=form,user_id=user_id))
    else :
        return render_template('index.html',stage=stage,form=form,user_id=user_id)

################################################################################################################################## 
################################################################################################################################## 
@app.route('/playlist',methods=['POST', 'GET'])
def playlist():
    stage = 3
    global timer
    timer = request.form.get('timer')
    
    #################################################################
    # Select Playlist
    global sp
    results = sp.current_user_playlists()
    export = []
    for result in results['items']:
        export_name = result['name']
        export_id = result['id']
        export_image = ""
        for image_result in result['images']:
            export_image = image_result['url']
            break
        export.append([export_name,export_id,export_image])

    form = PlaylistForm()

    return render_template('playlist.html',stage=stage,timer=timer,results=results,exports=export,form=form)


################################################################################################################################## 
################################################################################################################################## 
@app.route("/playlistRoute/", methods=['POST', 'GET'])
def playlistRoute():
    global playlist_id
    stage = 4
    if request.method == 'POST':
        playlist_id = request.form.get('playlist_id')
        return redirect(url_for('play', stage=stage, title='Music Timer for Spotify', playlist_id=playlist_id, timer=timer))

################################################################################################################################## 
################################################################################################################################## 
@app.route('/play',methods=['POST', 'GET'])
def play():
    stage = 4
    global playlist_id
    global timer
    timer = float(timer)*60000 # convert from minutes to ms
    playlist_id = request.args.get('playlist_id')
    #################################################################
    # Select Song
    global sp
    results = sp.playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', ))
    # Find song length that is closest to given timer
    difference_to_timer = float(abs(results['items'][0]['track']['duration_ms'] - float(timer)))   
    play_track_index = 0
    for count, track_results in enumerate(results['items']):
        current_track_difference = float(abs(track_results['track']['duration_ms'] - float(timer)))
        if current_track_difference < difference_to_timer:
            play_track_index = count
            difference_to_timer = current_track_difference

    play_track_id = [results['items'][play_track_index]['track']['uri']]
    playlist_length = results['items'][play_track_index]['track']['duration_ms']

    songs_in_playlist = int(results['total'])-1
    while float(timer) > float(playlist_length) and float(timer) - float(playlist_length) > 15000: #15 seconds
        if play_track_index == songs_in_playlist:
            play_track_index = 0
        else:
            play_track_index += 1
        play_track_id.append(results['items'][play_track_index]['track']['uri'])
        playlist_length += float(results['items'][play_track_index]['track']['duration_ms'])

    #################################################################
    # add the song(s) we want to the playlist
    global timerPlaylistId
    global user_id
    sp.user_playlist_add_tracks(user_id, playlist_id=timerPlaylistId, tracks=play_track_id)

    #################################################################
    # Play Song
    playlistUri = "spotify:playlist:" + timerPlaylistId
    sp.start_playback(context_uri=playlistUri)

    return redirect(url_for('countdown', stage=stage, title='Music Timer for Spotify', playlist_id=playlist_id, timer=timer))

################################################################################################################################## 
################################################################################################################################## 
@app.route('/countdown',methods=['POST', 'GET'])
def countdown():
    return render_template('countdown.html', title='Music Timer for Spotify', timer=timer)

################################################################################################################################## 
################################################################################################################################## 
@app.route('/stop',methods=['POST', 'GET'])
def stop():

    sp.pause_playback(device_id=None)

    def clearPlaylist():
        current_timer_playlist_songs = sp.playlist_items(playlist_id=timerPlaylistId, fields="items(track(id))")
        trackIds = list()
        for track in current_timer_playlist_songs["items"]:
            trackIds.append(track["track"]["id"])
        sp.playlist_remove_all_occurrences_of_items(playlist_id=timerPlaylistId, items=trackIds)

    clearPlaylist()

    # print(0)
    # play_track_id = ['spotify:track:1tFL456Lotpvnk8gCfZQOQ']
    # sp.user_playlist_add_tracks(user_id, playlist_id=timerPlaylistId, tracks=play_track_id)
    # playlistUri = "spotify:playlist:" + timerPlaylistId
    # print(1)
    # sp.start_playback(context_uri=playlistUri)
    # print(2)
    # # Stop alarm after 10 seconds
    # time.sleep(10)
    # print(3)
    # sp.pause_playback(device_id=None)
    # clearPlaylist()

    return redirect(url_for('index'))