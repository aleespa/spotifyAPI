import spotipy
from spotipy.oauth2 import SpotifyOAuth

import tomllib

with open("credentials.toml", "rb") as f:
    data = tomllib.load(f)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        redirect_uri=data["redirect_uri"],
        scope="playlist-modify-public playlist-modify-private user-library-read"
    )
)

tracks = []
results = sp.current_user_saved_tracks()
while results:
    tracks.extend(results['items'])
    results = sp.next(results)

specific_year = "1968"  # Replace with the desired year
filtered_tracks = []

for item in tracks:
    track = item['track']
    release_year = track['album']['release_date'][:4]
    if release_year == specific_year:
        filtered_tracks.append(track)


playlist_name = "My New Playlist"
playlist_description = "Created with Python and Spotipy!"
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

playlist_id = playlist['id']
sp.playlist_add_items(playlist_id, filtered_tracks)
