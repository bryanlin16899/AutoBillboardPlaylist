from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? format: YYYY-MM-DD\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

rqst = requests.get(URL)
web_page = rqst.text
soup = BeautifulSoup(web_page, "html.parser")
songs_tag = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song.getText() for song in songs_tag]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date}Billboard 1-100",
    public="False",
    description="test."
)
print(playlist)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uris,
)


