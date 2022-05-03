#!/usr/bin/python3.6

import requests


class YoutubeApi:
    """A class for interacting with the youtube api."""

    def __init__(self, my_api_key, yt_username):
        self.my_api_key_url = f"key={my_api_key}"
        self.yt_username = yt_username
        self.yt_api_root = "https://youtube.googleapis.com/youtube/v3/"

    def _make_api_request(self, url, request_type):
        try:
            api_request = getattr(requests, request_type)(
                url, headers={"Accept": "application/json"}
            )
            api_request.raise_for_status()
            api_request_json = api_request.json()
            api_request_json = api_request_json["items"]
        except Exception as query_error:
            print(f"Lookup attempt for url {url} failed with exception {query_error}")
            api_request_json = {"fail": True}

        return api_request_json

    def _get_my_user(self):
        my_user_url = (
            f"{self.yt_api_root}channels?forUsername={self.yt_username}&"
            + self.my_api_key_url
        )
        user_details = self._make_api_request(my_user_url, "get")
        user_id = user_details[0]["id"]

        return user_id

    def _get_users_playlists(self, user_id):
        my_playlist_url = (
            f"{self.yt_api_root}playlists?channelId={user_id}&" + self.my_api_key_url
        )
        playlist_details = self._make_api_request(my_playlist_url, "get")

        # Use list comprehension to filter out playlist ids from list of dictionaries
        playlist_id_list = [x["id"] for x in playlist_details if "id" in x]

        return playlist_id_list

    def _get_playlist_videos(self, playlist_id_list):
        playlist_videos = {}
        for playlist_id in playlist_id_list:
            my_playlistitem_url = (
                f"{self.yt_api_root}playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&"
                + self.my_api_key_url
            )
            playlist_contents = self._make_api_request(my_playlistitem_url, "get")
            playlist_videos[playlist_id] = playlist_contents

        return playlist_videos

    def write_to_csv(self):
        user_id = self._get_my_user()
        playlist_id_list = self._get_users_playlists(user_id)
        playlist_videos = self._get_playlist_videos(playlist_id_list)

        with open("playlist_results.csv", "w", encoding="utf-8") as result_file:
            result_file.write("video_title,video_id,playlist_id,publish_date\n")
            for playlist_id, video_dict in playlist_videos.items():
                for yt_video in video_dict:
                    try:
                        video_details = f'{str(yt_video["snippet"]["title"]).replace(",", "").lower()},{str(yt_video["snippet"]["resourceId"]["videoId"]).replace(",", "").lower()},{playlist_id},{str(yt_video["snippet"]["publishedAt"]).replace(",", "")}'
                        result_file.write(video_details + "\n")
                    except KeyError:
                        print(f"Error when processing values for item: {video_dict}")


if __name__ == "__main__":
    from yt_val import mkey, muser

    youtube_instance = YoutubeApi(mkey, muser)
    youtube_instance.write_to_csv()
