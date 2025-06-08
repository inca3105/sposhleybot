import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем ключи из .env
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Настраиваем соединение с API Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_track_info(spotify_url):
    try:
        # Получаем ID трека из ссылки
        parsed = urlparse(spotify_url)
        track_id = parsed.path.split('/')[-1]

        # Получаем информацию о треке
        track = sp.track(track_id)
        title = track["name"]
        artist = track["artists"][0]["name"]
        return f"{artist} - {title}"
    except Exception as e:
        return f"Ошибка: {e}"