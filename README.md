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
- [Refer to issues](https://github.com/Alex-Draper/SpotifyMusicTimer/issues)