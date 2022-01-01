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

# results = sp.current_user_saved_tracks()

results = sp.current_user_playlists()

#print(results)
#print(results["items"])

print ("SELECT PLAYLIST")
print ("---------------")
for count, playlist_results in enumerate(results['items']):
    # print (count)
    # print (playlist_results)
    print (str(count) +": "+ playlist_results['name'])

playlist_selection = int(input("Enter playlist number: "))
playlist_id = results['items'][playlist_selection]['id']
# for idx, item in enumerate(results["items"]):
#     track = item["track"]
# print(idx, track["artists"][0]["name"], " - ", track["name"])
