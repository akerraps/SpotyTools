import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def log_in():

    try:
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id= CLIENT_ID, client_secret= CLIENT_SECRET))
    except spotipy.oauth2.SpotifyOauthError as e:
        if "No client_id" in str(e):
            print("No client ID")
            exit(1)
        elif "No client_secret" in str(e):
            print ("No client secret")
            exit(1)
        else:
            print(f"Spotify Error: {str(e)}")
            exit(1)
    return spotify

def get_tracks(id):
    spotify = log_in()
    try:
        playlist_info = spotify.playlist( "https://open.spotify.com/playlist/" + id)
    except spotipy.exceptions.SpotifyException as e:
        if 'Invalid base62 id' in str(e):
            print(f"Error: Invalid playlist ID: {id}")
            exit(1)
        else:
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
            'Song Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Duration (ms)': track['duration_ms'],
            'Popularity': track['popularity'],
            'Added At': item['added_at']
        }
        track_data.append(track_info)

    df = pd.DataFrame(track_data)

    return df