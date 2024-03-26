import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import pprint

from methods import is_valid_date_format

print("Turn on your vpn")
travel_date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

is_valid = is_valid_date_format(travel_date)

if not is_valid:
    raise Exception("This format is invalid")

response = requests.get(f'https://www.billboard.com/charts/hot-100/{travel_date}/')

if response.status_code != 200:
    raise Exception("I can't get the website :(")

soup = BeautifulSoup(response.text, "html.parser")

songs_list = \
    [{"name": song_tag.select_one('h3').getText().strip(),
      "artist": song_tag.select_one('span').getText().strip()}
     for song_tag
     in soup.select("li.o-chart-results-list__item:has(h3#title-of-a-story)")]

input("Turn off the vpn and press enter")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="995b732962074fdb897055082ca5330d",
                                               client_secret="7db0eeabd5b94a57b95761f0eb023ad5",
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))

user = sp.current_user()
song_uris = []
year = travel_date.split('-')[0]
for song in songs_list:
    try:
        sp_search_result = sp.search(f"track:{song['name']} year:{year}", limit=1)
        url = sp_search_result['tracks']['items'][0]['uri']
        song_uris.append(url)
    except IndexError as error:
        print(f'{song} is not available on spotify')


if len(song_uris) > 0:
    playlist = sp.user_playlist_create(user=user['id'], name=f"{travel_date} Billboard 100", public=False)
    result = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)