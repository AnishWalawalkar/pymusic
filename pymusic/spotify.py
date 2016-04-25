import requests
import os

AUTH_URI = 'https://accounts.spotify.com/api/token'
BASE_URI = 'https://api.spotify.com'

def get_spotify_token():
    res = requests.post(
        AUTH_URI,
        data={'grant_type': 'client_credentials'},
        auth=(os.environ.get('SPOTIPY_CLIENT_ID'), os.environ.get('SPOTIPY_CLIENT_SECRET'))
    )
    return res.json()['access_token']

def get_featured_playlists(access_token):
    res = requests.get(
        BASE_URI + '/v1/browse/featured-playlists',
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
    )

    return res.json()


def get_tracks(access_token, playlist_id):
    res = requests.get(
        BASE_URI + '/v1/users/spotify/playlists/{}'.format(playlist_id),
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
        params= {'limit': 100}
    )

    spotify_tracks = res.json()['tracks']['items']
    output = []

    for track in spotify_tracks:
        name = track['track']['name']
        artists = [artist['name'] for artist in track['track']['artists']]
        output.append('{} {}'.format(name, ' '.join(artists)))

    return output


# def main():
#     access_token = get_spotify_token()
#     with open('songs.json', 'w') as open_file:
#         import json
#         string_data = json.dumps(get_tracks(access_token, '5FJXhjdILmRA2z5bvz4nzf'), indent=2)
#         open_file.write(string_data)

# if __name__ == '__main__':
#     main()




