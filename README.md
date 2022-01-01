# SpotifyMusicTimer
Timer that plays songs for a given length of time from spotify

1. ask user for timer length
2. get user's playlists https://developer.spotify.com/console/get-current-user-playlists/?limit=&offset=, returns a json file
3. from there users can select a playlist (we'll grab the playlist id from json)
4. get the list of songs in playlist https://developer.spotify.com/console/get-playlist-tracks/
5. sort them by duration_ms
6. find right song
7. add song to playback queue (so we have to assume user has nothing in queue for now, since we cannot clear the queue) https://developer.spotify.com/console/post-queue/
8. start playback https://developer.spotify.com/console/put-play/
9. stop playback when timer is up https://developer.spotify.com/console/put-pause/