'''module to work with the youtubetomp3 api'''

import requests

class Youtube(object):

    api_url = 'https://www.googleapis.com/youtube/v3/search'
    watch_url = 'http://www.youtube.com/watch?v={}'

    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve_video_link(self, song):
        payload = {
            'key': self.api_key,
            'part': 'snippet',
            'type': 'video',
            'order': 'relevance',
            'q': ' '.join(song.values()),
            'maxResults': 10
        }

        resp = requests.get(Youtube.api_url, params=payload)

        if resp.status_code == 200:
            data_dict = resp.json()
            video_id = data_dict.get(
                'items', [])[0].get('id', {}).get('videoId', None)
            if video_id is not None:
                return Youtube.watch_url.format(video_id)

        return None

    def __call__(self, song):
        return self.retrieve_video_link(song)


class Mp3(object):

    api_url = 'http://www.youtubeinmp3.com/fetch/'

    def __init__(self, output_directory):
        self.output_directory = output_directory

    @staticmethod
    def retrieve_song_link(youtube_link):

        payload = {
            'format': 'JSON',
            'video': youtube_link
        }

        resp = requests.get(Mp3.api_url, params=payload)

        if resp.status_code == 200:
            return resp.json()


    def download_music_stream(self, song_dict):
        song_link = song_dict.get('link', None)
        song_title = song_dict.get('title', 'Unknown')
        if song_link is None:
            return

        resp = requests.get(song_link, stream=True)

        if resp.status_code == 200:
            song_output = self.output_directory + song_title + '.mp3'
            with open(song_output, 'wb') as output_file:
                for content in resp.iter_content(chunk_size=2048):
                    output_file.write(content)


    def __call__(self, youtube_link):
        self.download_music_stream(Mp3.retrieve_song_link(youtube_link))
