I've created this utility to help me identify deleted/removed videos on my youtube playlists. 

This setup requires an API Key and your youtube username in a file named yt_val.py. 

To get an api key: https://developers.google.com/youtube/registering_an_application 

# Example file: 
vi yt_val.py 
muser = "youtube_username_here"
mkey = "api_key_here"


The results of the search will appear in a csv named playlist_results.csv. 
This will allow you to identify video names if any items are removed going forward, while also providing upload dates and video id's for removed items that can be identified on the wayback machine. 

Wayback machine: https://archive.org/web/