'''module to work with the youtubetomp3 api'''

import requests

class Mp3(object):

    api_url = 'http://www.youtubeinmp3.com/fetch/'

    def __init__(self, output_directory):
        self.output_directory = output_directory

    def retrieve_song_link(self, youtube_link):

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
            with open(song_output, 'wb') as file:
                for content in resp.iter_content(chunk_size=2048):
                    file.write(content)


    def __call__(self, youtube_link):
        self.download_music_stream(self.retrieve_song_link(youtube_link))

