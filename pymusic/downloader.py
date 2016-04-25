import spotify
from youtube2mp3 import Youtube, Mp3
from threading import Thread


def download_song(song):
    youtube = Youtube()
    youtube_link = youtube(song)
    mp3 = Mp3(youtube_link, output_directory='/Users/JustAnish/Documents/songs/')
    mp3()

def get_songs():
    access_token = spotify.get_spotify_token()
    songs = spotify.get_tracks(access_token, '3fCn2nqmX6ZnYUe9uoty98')

    threads = []

    for song in songs:
        thread = Thread(target=download_song, args=(song,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    get_songs()

if __name__ == '__main__':
    main()
