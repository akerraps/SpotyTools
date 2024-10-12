from flask import Flask, render_template
from get_api import get_tracks
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    playlist_id =os.getenv('PLAYLIST_ID')
    df = get_tracks(playlist_id)
    tracks = df.to_dict(orient='records')
    return render_template('index.html', tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True, port=5000)