from flask import Flask, render_template, redirect, request, session, url_for
from get_api import get_user_spotify, get_tracks_from_playlist, get_playlists
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def login():
    global spotify
    auth_data = get_user_spotify()
    if auth_data['auth_url']:
        return redirect(auth_data['auth_url'])
    spotify = auth_data['spotify']
    return redirect(url_for('index'))

@app.route('/playlists')
def index():
    global spotify

    if 'spotify' not in globals() or spotify is None:
        print('Spotify client no está definido, redirigiendo al login')
        return redirect(url_for('login'))

    playlists = get_playlists(spotify)
    return render_template('index.html', playlists=playlists)

@app.route('/tracks', methods=['POST'])
def tracks():
    global spotify

    if 'spotify' not in globals() or spotify is None:
        print('Spotify client no está definido, redirigiendo al login')
        return redirect(url_for('login'))

    playlist_id = request.form['list']
    tracks = get_tracks_from_playlist(spotify, playlist_id)
    return render_template('show_tacks.html', tracks=tracks)


@app.route('/list-playlists')
def playlists():
    auth_data = get_user_spotify()
    if auth_data['auth_url']:
        # Redirigir al usuario a Spotify para autenticarse
        return redirect(auth_data['auth_url'])

    spotify = auth_data['spotify']

    if spotify:
        playlists = get_playlists(spotify)
        return render_template('show_playlists.html', tracks=playlists)
    else:
        return redirect(url_for('login'))

@app.route('/callback')
def callback():
    from get_api import create_spotify_oauth
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    session['token_info'] = token_info
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)