# Spotify Music Timer
Timer that plays songs for a given length of time from spotify

## ⚡Progress⚡
- [x] MVP Flask app
- [ ] Hosted on Heroku
- [ ] Alexa integration
- [ ] Submit a Spotify quota extension request

## ❗Known Issues❗
- Lines 193 to 204 of routes.py do not work as expected, currently commented out
  - Loops between print 0 1 2, pausing and restarting the timer track for an unknown reason
  - Will result in an error
- App will sometimes return music tracks that are region locked and unplayable by user
- Excessive timer length can result in an error, especially when selecting playlists with short tracks
- Playlist images do not display correctly if in a non 1:1 aspect ratio
- Long playlist names will result in irregular card lengths
- Currently operates on a whitelist for users, no public access
