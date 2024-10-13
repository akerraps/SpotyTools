from flask import Flask, render_template, redirect, request, session, url_for
from get_api import get_user_spotify, get_tracks_from_spotify  # Importamos la función correcta
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Clave secreta para manejar sesiones
load_dotenv()


@app.route('/')
def index():
    auth_data = get_user_spotify()
    if auth_data['auth_url']:
        # Redirigir al usuario a Spotify para autenticarse
        return redirect(auth_data['auth_url'])

    spotify = auth_data['spotify']

    if spotify:
        playlist_id = os.getenv('PLAYLIST_ID')  # Obtener el ID de la playlist del entorno
        df = get_tracks_from_spotify(spotify, playlist_id)  # Obtener pistas usando el objeto spotify
        tracks = df.to_dict(orient='records')  # Convertir a diccionario
        print('test')
        return render_template('index.html', tracks=tracks)
    else:
        return redirect(url_for('login'))


@app.route('/callback')
def callback():
    from get_api import create_spotify_oauth
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Guardar el token en la sesión
    session['token_info'] = token_info
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)