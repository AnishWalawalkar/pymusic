'''module to work with the youtube api'''

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

