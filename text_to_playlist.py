import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_playlist(songs, playlist_name, sp):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user = user_id, name = playlist_name, public = False)
    playlist_id = playlist['id']

    for song in songs:
        results = sp.search(q = song, limit = 1)
        track_id = results['tracks']['items'][0]['id']
        sp.playlist_add_items(playlist_id, [track_id])

    print(f"Playlist '{playlist_name}' created successfully!")

def query_user(sp):
    playlist_name = input("Enter playlist name: ")
    print("Enter list of songs, separated by newlines. End your input with an empty line.")
    songs = []
    while True:
        song = input()
        if not song:
            break
        songs.append(song)
    create_playlist(songs, playlist_name, sp)

if __name__ == '__main__':

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    CLIENT_ID = config['client_id']
    CLIENT_SECRET = config['client_secret']

    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = 'https://localhost:8888/callback',
        scope = 'playlist-modify-private'
    ))
    
    query_user(sp)