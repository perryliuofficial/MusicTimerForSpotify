import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id="",
        client_secret="",
        redirect_uri="http://localhost:8080/",
    )
)

# results = sp.current_user_saved_tracks()

results = sp.current_user_saved_tracks()

print(results)

# for idx, item in enumerate(results["items"]):
#     track = item["track"]
# print(idx, track["artists"][0]["name"], " - ", track["name"])
