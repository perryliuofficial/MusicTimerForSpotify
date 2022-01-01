from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID=config('CLIENT_ID')
CLIENT_SECRET=config('CLIENT_SECRET')
REDIRECT_URI=config('REDIRECT_URI')

scope = "user-library-read playlist-read-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
)


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
print (play_track_id)


#################################################################
# Play Song
# Start Timer


# When time is up, stop current song and play song ID 5mfyfIaXH6S545I5csyhoU (Crystal Maze - Force Field)
