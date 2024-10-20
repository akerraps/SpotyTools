import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "playlist-read-private playlist-read-collaborative"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

def get_user_spotify():
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return {'auth_url': auth_url, 'spotify': None}
    else:
        spotify = spotipy.Spotify(auth=token_info['access_token'])
        return {'auth_url': None, 'spotify': spotify}


def get_tracks_from_playlist(spotify, playlist_id):
    try:
        playlist_info = spotify.playlist( "https://open.spotify.com/playlist/" + playlist_id)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify Error: {str(e)}")
        exit(1)

    tracks = playlist_info['tracks']
    all_tracks = tracks['items']
    while tracks['next']:
        tracks = spotify.next(tracks)
        all_tracks.extend(tracks['items'])

    track_data = []
    for item in all_tracks:
        track = item['track']
        track_info = {
            'song_name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'duration': track['duration_ms']
        }
        track_data.append(track_info)

    df = pd.DataFrame(track_data)
    return df

def get_playlists (spotify):
    playlist_general_info = spotify.current_user_playlists()
    playlists=playlist_general_info['items']

    playlist_data=[]
    for item in playlists:
        playlist_info={
            'name': item['name'],
            'playlist_id':item['id'],
            'track_count':item['tracks']['total']
        }
        playlist_data.append(playlist_info)
    return playlist_data