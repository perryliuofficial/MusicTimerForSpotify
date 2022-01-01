from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
        name="Timer Playlist Test",
        public=False,
        collaborative=False,
        description="Playlist Timer Test",
    )
    timerPlaylistId = response["id"]
#     print("Created!")
# else:
#     print("timer playlist does exist")


#################################################################
# clear the playlist to ensure only the songs we want to play are there

current_timer_playlist_songs = sp.playlist_items(
    playlist_id=timerPlaylistId, fields="items(track(id))"
)

trackIds = list()

for track in current_timer_playlist_songs["items"]:
    trackIds.append(track["track"]["id"])

#print(trackIds)

sp.playlist_remove_all_occurrences_of_items(playlist_id=timerPlaylistId, items=trackIds)


#################################################################
# Ask for timer duration
timer = float(input("Timer Duration in minutes: "))
timer = timer*60000 # convert to ms


#################################################################
# Select Playlist
results = sp.current_user_playlists()

print ("SELECT PLAYLIST")
print ("---------------")
for count, playlist_results in enumerate(results['items']):
    print (str(count) +": "+ playlist_results['name'])

playlist_selection = int(input("Enter playlist number: "))
playlist_id = results['items'][playlist_selection]['id']


#################################################################
# Select Song
results = sp.playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market="GB", additional_types=('track', ))

# Find song length that is closest to given timer
difference_to_timer = abs(results['items'][0]['track']['duration_ms'] - timer)   
play_track_index = 0
for count, track_results in enumerate(results['items']):
    current_track_difference = abs(track_results['track']['duration_ms'] - timer)
    if current_track_difference < difference_to_timer:
        play_track_index = count
        difference_to_timer = current_track_difference

# If timer - song duration > 15 seconds then add another song to queue
play_track_id = [results['items'][play_track_index]['track']['uri']]
if difference_to_timer > 15000: #15 seconds
    if play_track_index == 0:
        play_track_id.append(results['items'][play_track_index+1]['track']['uri'])
    else:
        play_track_id.append(results['items'][play_track_index-1]['track']['uri'])
#print (results['items'][0])
#print (play_track_id)


#################################################################
# add the song(s) we want to the playlist
sp.user_playlist_add_tracks(user_id, playlist_id=timerPlaylistId, tracks=play_track_id)


#################################################################
# Play Song
playlistUri = "spotify:playlist:" + timerPlaylistId
sp.start_playback(context_uri=playlistUri)

# Start Timer


# When time is up, stop current song and play song ID 1tFL456Lotpvnk8gCfZQOQ
