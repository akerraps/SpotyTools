from get_api import get_tracks
from dotenv import load_dotenv
import os

load_dotenv()

PLAYLIST_ID = os.getenv('PLAYLIST_ID')
OUTPUT = os.getenv('OUTPUT')

def main():
    playlist_id =PLAYLIST_ID
    tracks=get_tracks(playlist_id)
    try:
        tracks.to_excel(OUTPUT, index=False)
    except OSError as e:
        if "non-existent directory" in str(e):
            print ("The directory doesn't exist")
            exit(1)
        else:
            print(f"OS Error: {str(e)}")
            exit(1)

# Ejecutar la función principal
if __name__ == "__main__":
    main()