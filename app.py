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
#print (results['items'][0]['track']['duration_ms'])

difference_to_timer = abs(results['items'][0]['track']['duration_ms'] - timer)
#print ("diff to timer: " + str(difference_to_timer))
    
for count, track_results in enumerate(results['items']):
    #print(str(count)+ ": " + str(track_results['track']['duration_ms']))
    current_track_difference = abs(track_results['track']['duration_ms'] - timer)
    #print ("curr diff: " + str(current_track_difference))
    if current_track_difference < difference_to_timer:
        play_track_id = count
        difference_to_timer = current_track_difference

#print ("id: " + str(play_track_id))

