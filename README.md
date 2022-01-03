# Spotify Music Timer
Timer that plays songs for a given length of time from spotify

## ⚡Progress⚡
- [x] MVP Flask app
- [ ] Hosted on Heroku
  - Unless the repo sits within a GitHub organisation, only the repo owner can set up automated deployment to Heroku
- [ ] Alexa integration
- [ ] Submit a Spotify quota extension request

## 💡How It Works💡
- Refer to [documentation](https://github.com/Alex-Draper/SpotifyMusicTimer/tree/dev/documentation/design) for more information
- This app is currently in development mode and is in whitelist mode. To use the app:
  - Set up a Spotify dev account
  - Generate client id/ secret
  - Add redirect uri under settings
- toplevel.py initialises app
- app/__init__.py initialises app and sets up global variables
- .env (gitignored) stores all environmental variables. To set it up:
  -  CLIENT_ID=000000000000000000000000
  -  CLIENT_SECRET=0000000000000000000
  -  REDIRECT_URI='http://localhost:8080/'
  -  FLASK_WTF_KEY='random-string'
- app/routes.py manages app logic and flow, this is where the bulk of the code is
- app/templates for html files

## ❗Known Issues❗
- Lines 193 to 204 of routes.py do not work as expected, currently commented out
  - Loops between print 0 1 2, pausing and restarting the timer track for an unknown reason
  - Will result in an error
- App will sometimes return music tracks that are region locked and unplayable by user
- Excessive timer length can result in an error, especially when selecting playlists with short tracks
- Spotify can sometimes fail to detect active devices for playback
- Playlist images do not display correctly if in a non 1:1 aspect ratio
- Long playlist names will result in irregular card lengths
- Currently operates on a whitelist for users, no public access
- In extremely rare cases Spotify can fail to update playlist, resulting in the same track over and over again
  - Deleting the playlist will resolve the issue
- Spotify API errors result in error message on webpage (lack of error handling)
- Significant refactoring and code cleanup required
