import requests
from threading import Thread
import time

YOUTUBE_API_KEY = 'AIzaSyDd9I_b3Orr9IOGdrWSHFJn1RmKj6mWp_I'
YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
MP3_URL = 'http://www.youtubeinmp3.com/fetch/'


def youtube_song_url(song):
    '''return youtube video id'''

    payload = {
        'key': YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'order': 'relevance',
        'q': song
    }

    req = requests.get(YOUTUBE_URL, params=payload)

    if req.status_code == 200:
        return 'http://www.youtube.com/watch?v={}'.format(req.json()['items'][0]['id']['videoId'])

    return None

def mp3_url(youtube_song_url):

    payload = {
        'format': 'JSON',
        'video': youtube_song_url
    }

    req = requests.get(MP3_URL, params=payload)

    if req.status_code == 200:
        return req.json()['link']

    return None

def download_song(url, song_name):
    req = requests.get(url, stream=True)

    with open('songs/'+song_name, 'wb') as output_file:
        for content in req.iter_content(chunk_size=2048):
            if content:
                output_file.write(content)

def performer(song):
    youtube_watch_url = youtube_song_url(song)
    if youtube_watch_url is not None:
        mp3 = mp3_url(youtube_watch_url)
        if mp3 is not None:
            download_song(mp3, song+'.mp3')

def main():
    songs = [
        'cake by the ocean',
        'paradise',
        'my house',
        'I know what you did last summer',
        'me, myself & I',
        'when the beat drops out',
        'work',
        'pillowtalk',
        'lush life',
        'hide away',
        'stay',
        'all my friends',
        'faded',
        'middle',
        'running out',
        'lay it all on me',
        '7 years',
        'I took a pill in ibiza',
        'youth',
        'never forget you',
        'bang my head',
        'sorry',
        'hollow'
    ]

    threads = []

    for song_name in songs:
        threads.append(Thread(target=performer, args=(song_name,)))

    start_time = time.time()

    _ = [thread.start() for thread in threads]
    _ = [thread.join() for thread in threads]

    print('Time take to download songs: {}'.format(time.time()-start_time))


if __name__ == '__main__':
    main()
