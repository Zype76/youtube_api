#!/usr/bin/python3.6

import requests


class YoutubeApi:
    """A class for interacting with the youtube api."""

    def __init__(self, my_api_key, yt_username):
        self.my_api_key_url = f"key={my_api_key}"
        self.yt_username = yt_username
        self.yt_api_root = "https://youtube.googleapis.com/youtube/v3/"

    def _make_request(self, url, request_type):
        try:
            headers = {"Accept": "application/json"}
            request_result = getattr(requests, request_type)(url, headers=headers)
            request_result.raise_for_status()
            request_result_json = request_result.json()
            request_result_json = request_result_json["items"]
        except Exception as query_error:
            print(f"Lookup attempt for url {url} failed with exception {query_error}")
            request_result_json = {"fail": True}

        return request_result_json

    def _get_my_user(self):
        my_user_url = (
            f"{self.yt_api_root}channels?forUsername={self.yt_username}&"
            + self.my_api_key_url
        )
        user_details = self._make_request(my_user_url, "get")
        return user_details[0]["id"]

    def _get_my_playlists(self):
        user_id = self._get_my_user()
        my_playlist_url = (
            f"{self.yt_api_root}playlists?channelId={user_id}&" + self.my_api_key_url
        )
        playlist_details = self._make_request(my_playlist_url, "get")
        playlist_details = playlist_details[0]["id"]
        return playlist_details

    def get_playlist_videos(self):
        playlist_id = self._get_my_playlists()

        my_playlistitem_url = (
            f"{self.yt_api_root}playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&"
            + self.my_api_key_url
        )
        playlist_contents = self._make_request(my_playlistitem_url, "get")
        return playlist_contents

    def write_to_csv(self):
        playlist_videos = self.get_playlist_videos()
        with open("test.csv", "w", encoding="utf-8") as result_file:
            result_file.write("Video_title\n")
            for video in playlist_videos:
                result_file.write(str(video["snippet"]["title"] + "\n"))


if __name__ == "__main__":
    from yt_val import mkey, muser
    youtube_instance = YoutubeApi(mkey, muser)
    youtube_instance.write_to_csv()
