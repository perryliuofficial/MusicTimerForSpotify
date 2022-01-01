from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")

scope = "user-library-read playlist-read-private playlist-modify-private user-modify-playback-state"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
)


# Step 1 get user id
results = sp.current_user()
user_id = results["id"]

# Step 2 check if Timer playlist exists, if not create it. Also get the playlist id
results = sp.current_user_playlists()
playlist_items = results["items"]


timerPlaylistExists = False
timerPlaylistId: str

for item in playlist_items:
    name = item["name"]
    if name == "Timer Playlist Test":
        timerPlaylistExists = True
        timerPlaylistId = item["id"]
        break

print("---------")

if not timerPlaylistExists:
    print("Timer Test Playlist does not exist! Creating it...")
    response = sp.user_playlist_create(
        user=user_id,
        name="Timer Playlist Test",
        public=False,
        collaborative=False,
        description="Playlist Timer Test",
    )
    timerPlaylistId = response["id"]
    print("Created!")
else:
    print("timer playlist does exist")


# step 3 - clear the playlist to ensure only the songs we want to play are there

current_timer_playlist_songs = sp.playlist_items(
    playlist_id=timerPlaylistId, fields="items(track(id))"
)

trackIds = list()

for track in current_timer_playlist_songs["items"]:
    trackIds.append(track["track"]["id"])


print(trackIds)

sp.playlist_remove_all_occurrences_of_items(playlist_id=timerPlaylistId, items=trackIds)

# step 4 add the song(s) we want to the playlist
test_songs = [
    "spotify:track:70ebKSMHvkUSg7JXgUz74Q",
    "spotify:track:10nqz67NQWWa7XPq7ycihi",
    "spotify:track:5awDNL0otyBZIpgjGnO49w",
]

sp.user_playlist_add_tracks(user_id, playlist_id=timerPlaylistId, tracks=test_songs)

# step 5 play the playlist
playlistUri = "spotify:playlist:" + timerPlaylistId
sp.start_playback(context_uri=playlistUri)
