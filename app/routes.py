from flask import render_template,request
from app import app
from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Music Timer for Spotify', user=user)
@app.route('/timer', methods = ['POST', 'GET'])
def timer():
    CLIENT_ID=config('CLIENT_ID')
    CLIENT_SECRET=config('CLIENT_SECRET')
    REDIRECT_URI=config('REDIRECT_URI')

    scope = "user-library-read playlist-read-private playlist-modify-private user-modify-playback-state"
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
    #print("user: "+user_id)

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

    #print("---------")

    if not timerPlaylistExists:
        # print("Timer Test Playlist does not exist! Creating it...")
        response = sp.user_playlist_create(
            user=user_id,
            name="Spotify Music Timer",
            public=False,
            collaborative=False,
            description="Spotify Music Timer",
        )
        timerPlaylistId = response["id"]
    #     print("Created!")
    # else:
    #     print("timer playlist does exist")


    #################################################################
    # clear the playlist to ensure only the songs we want to play are there
    def clearPlaylist():
        current_timer_playlist_songs = sp.playlist_items(playlist_id=timerPlaylistId, fields="items(track(id))")
        trackIds = list()
        for track in current_timer_playlist_songs["items"]:
            trackIds.append(track["track"]["id"])
        sp.playlist_remove_all_occurrences_of_items(playlist_id=timerPlaylistId, items=trackIds)

    clearPlaylist()

    try:
        timer = int(request.form.get('InputMinutes'))
    except:
        timer = 5 # Default

    timer = timer*60000 # convert to ms
    print(timer)

    #################################################################
    # Select Playlist
    results = sp.current_user_playlists()

    # print ("SELECT PLAYLIST")
    # print ("---------------")
    # for count, playlist_results in enumerate(results['items']):
    #     print (str(count) +": "+ playlist_results['name'])

    # playlist_selection = int(input("Enter playlist number: "))
    # playlist_id = results['items'][playlist_selection]['id']

    return render_template('timer.html', title='Music Timer for Spotify')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html', title='Music Timer for Spotify')