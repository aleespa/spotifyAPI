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

for specific_year in ["1968" "1970", "1980", '1990', "2018", "2019",'2020', '2021', '2022', '2023']:
    filtered_tracks = []

    for item in tracks:
        track = item['track']
        release_year = track['album']['release_date'][:4]
        if release_year == specific_year:
            filtered_tracks.append(track)

    playlist_name = f"Playlist {specific_year}"
    playlist_description = "Created with Python and Spotipy!"
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

    print(filtered_tracks)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, [track['uri'] for track in filtered_tracks])
