# SpotifyMusicTimer
Timer that plays songs for a given length of time from spotify

1. ask user for timer length
2. get user's playlists https://developer.spotify.com/console/get-current-user-playlists/?limit=&offset=, returns a json file
3. from there users can select a playlist (we'll grab the playlist id from json)
4. get the list of songs in playlist https://developer.spotify.com/console/get-playlist-tracks/
5. sort them by duration_ms
6. find right song
7. add song to playback queue\* https://developer.spotify.com/console/post-queue/
8. start playback\* https://developer.spotify.com/console/put-play/
9. stop playback when timer is up https://developer.spotify.com/console/put-pause/

\* We cannot clear the current queue which might be problematic if user already has a song. However we can provide a context uri when starting playback, so we might be able to specify a song there?