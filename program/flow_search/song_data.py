import pandas as pd 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from apiclient.discovery import build
import json
import pprint
from bs4 import BeautifulSoup
from collections import defaultdict
import urllib.request as req
import string

Client_ID = 'your Client_ID'
Client_Secret = 'your secret key'
YOUTUBE_API_KEY = 'your API key'

spotify_client_id = 'your id'
spotify_client_secret = 'your secret key'
spotify_client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(spotify_client_id, spotify_client_secret)
spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

def reveal_key(key):
    if key == 0:
        return "C"  
    elif key == 1:
        return "C#"
    elif key == 2:
        return "D"
    elif key == 3:
        return "D#"
    elif key == 4:
        return "E"
    elif key == 5:
        return "F"
    elif key == 6:
        return "F#"
    elif key == 7:
        return "G"
    elif key == 8:
        return "G#"
    elif key == 9:
        return "A"
    elif key == 10:
        return "A#"
    elif key == 11:
        return "B"
    else:
        raise ValueError
    
def reveal_mode(mode):
    if mode == 1:
        return "Major"
    else:
        return "Minor"

def details(key,mode):
    return reveal_key(key) + " " +reveal_mode(mode)


def get_artist_image(name):
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_uri = artist_items['uri']
    artist_image = artist_items['images'][0]['url']
    return artist_image

def get_artist_popularity(name):
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_popularity = artist_items['popularity']
    return artist_popularity


def get_artist_copytights(name):
    labels_data = {}
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_id = artist_items['id']
    for i in range(len(spotify.artist_albums(artist_id,limit=10)['items'])):
        albums = spotify.artist_albums(artist_id,limit=10)['items'][i]['id']
        album_data = spotify.album(albums)
        labels = album_data['label']
        for j in range(len(labels)):
            if labels in labels_data:
                labels_data[labels] += 1 
            else:
                labels_data[labels] = 1
    labels_dic = sorted(labels_data.items(), key=lambda x:x[1],reverse=True)
    return labels_dic


def show_results(name):
    d = defaultdict(list)
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_uri = artist_items['uri']
    artist_name = artist_items['name']
    artist_id = artist_items['id']


    track_dict = {}
    artist_top_tracks = spotify.artist_top_tracks(artist_id)['tracks']
    for i in range(len(artist_top_tracks)):
        track_dict[artist_top_tracks[i]['name']] = artist_top_tracks[i]['id']
        track_id = track_dict[artist_top_tracks[i]['name']]
        track_details = spotify.audio_features(track_id)
        track_key = [d.get('key') for d in track_details]
        track_mode = [d.get('mode') for d in track_details]
        track_bpm = [d.get('tempo') for d in track_details]
        track_danceability = [d.get('danceability') for d in track_details]
        track_acousticness = [d.get('acousticness') for d in track_details]
        d[artist_top_tracks[i]['name']].append(details(track_key[0],track_mode[0]))
        d[artist_top_tracks[i]['name']].append(str(round(track_bpm[0])))
        d[artist_top_tracks[i]['name']].append(str(artist_top_tracks[i]['popularity']))
        d[artist_top_tracks[i]['name']].append(artist_top_tracks[i]['uri'])            
    return d

def youtube_tutorials(name):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
    part='snippet',
    q='how to make music like' + name,
    type='video',
    maxResults = 3,
    ).execute()
    
    video_ids = []
    if len(search_response['items']) >= 3:
        for i in range(3):
            if name.upper() in search_response['items'][i]['snippet']['title'].upper() and 'HOW' in search_response['items'][i]['snippet']['title'].upper():
                video_ids.append(search_response['items'][i]['id']['videoId'])
    return video_ids


def get_artist_name(name):
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    return artist_name

"""
def sample_packs_recommend(name):
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_name_query = artist_name.replace(' ','%20')
    url = "https://www.adsrsounds.com/shop/?src=" + artist_name_query
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }
    request = req.Request(url=url, headers=headers)
    response = req.urlopen(request)
    parse_html = BeautifulSoup(response,'html.parser')
    sample_pack = {}
    title_lists = parse_html.find_all("a")
    title_list = []
    url_list = []
    for i in title_lists:
        title_list.append(i.string)
        url_list.append(i.attrs['href'])
    df_title_url = pd.DataFrame({'Title':title_list,'URL':url_list})
    df_notnull = df_title_url.dropna(how='any')
    df_packs = df_notnull['URL'].str.contains('/product/')
    as_result = df_notnull[df_packs]
    to_dict = as_result.to_dict('records')

    
    return to_dict

"""

def get_chord_progressions(name):
    spotapi_out = spotify.search(q=name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_name = artist_items['name']
    artist_name_query = artist_name.replace(' ','%20')
    url = "https://chordify.net/search/" + artist_name_query
    return url
