# Spotify Music Timer
Timer that plays songs for a given length of time from spotify, from your selected playlist.

## 💡To Run App Locally💡
- Clone or download repo.
- ```pip install Flask```
- ```pip install -U Flask-WTF```
- ```pip install spotipy```
- ```pip install python-decouple```
- Install any other required modules if you encounter an error when running the app.
- Ensure you have a Spotify user account.
- Create a [Spotify developer account](https://developer.spotify.com/dashboard/applications).
  - Create an app and generate client id/ secret.
  - Under app settings add a Redirect URI.
- Create a .env file in the root directory and populate it with info from above.
  - CLIENT_ID=000000000000000000000000
  - CLIENT_SECRET=00000000000000000000
  - REDIRECT_URI='http://localhost:8080/'
  - FLASK_WTF_KEY='random-string'
- ```flask run```
- Alternatively to run standalone_app.py which runs within the terminal:
  -  ```python standalone_app.py```

## 💡How It Works💡
- Refer to [documentation](https://github.com/Alex-Draper/SpotifyMusicTimer/tree/dev/documentation/design) for more information.
- toplevel.py initialises app.
- app/__init__.py initialises app and sets up global variables.
- .env (gitignored) stores all environmental variables.
- app/routes.py manages app logic and flow. This is where the bulk of the code is.
- app/templates for html files.

## ❗Known Issues❗
- [Refer to issues](https://github.com/Alex-Draper/SpotifyMusicTimer/issues)
