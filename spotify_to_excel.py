import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
OUTPUT = os.getenv('OUTPUT')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id= CLIENT_ID, client_secret= CLIENT_SECRET))


def get_tracks(id):
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
        tracks = spotify.next(tracks)  # Actualizamos tracks con la siguiente página
        all_tracks.extend(tracks['items'])  # Añadimos los nuevos items a la lista all_tracks

    track_data = []

    for item in all_tracks:
        track = item['track']
        track_info = {
            'Song Name': track['name'],
            'Artist': track['artists'][0]['name'],  # Primer artista
            'Album': track['album']['name'],
            'Duration (ms)': track['duration_ms'],
            'Popularity': track['popularity'],
            'Added At': item['added_at']  # Cuándo fue añadida a la playlist
        }
        track_data.append(track_info)

    # Crear un DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(track_data)

    return df

def main():
    playlist_id =PLAYLIST_ID
    tracks=get_tracks(playlist_id)
    print(tracks)
    tracks.to_excel(OUTPUT, index=False)

# Ejecutar la función principal
if __name__ == "__main__":
    main()