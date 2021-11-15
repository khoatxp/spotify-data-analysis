import sys
import json
import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'be6c9bede21a427eb7bc36544b630d16'
client_secret = 'ca9edb0705264512900c60b7a7913efe'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_ids(path):
    with open(path) as f:
        js = f.read()
        challenge_set = json.loads(js)

        unique_tracks = set()
        unique_albums = set()
        unique_artists = set()
        total_tracks = 0
        for playlist in challenge_set["playlists"]:
            for track in playlist["tracks"]:
                unique_tracks.add(track["track_uri"][14:])
                unique_albums.add(track["album_uri"])
                unique_artists.add(track["artist_uri"])
                total_tracks += 1
        print("total playlists:", len(challenge_set["playlists"]))
        print("total tracks:   ", total_tracks)
        print("unique tracks:  ", len(unique_tracks))
        print("unique albums:  ", len(unique_albums))
        print("unique artists: ", len(unique_artists))
        return unique_tracks


def get_audio_features(track_ids, chunk_size):
    audio_features_list = []
    for i in range(0, len(track_ids), chunk_size):    
        try:
            track_id_list = track_ids[i:i+chunk_size]
            results = sp.audio_features(track_id_list)
            results = [dict({'id':'None'}) if v is None else v for v in results]
            for result in results:
                del result['track_href']
                del result['analysis_url']
                del result['type']
                del result['uri']
            audio_features_list.extend(results)
        except Exception as e:
            print(e)
            continue
    return audio_features_list

def get_tracks_data(track_ids, chunk_size):
    tracks_data_list = []
    single_track_dict = {}
    for i in range(0, len(track_ids), chunk_size):    
        try:
            track_id_list = track_ids[i:i+chunk_size]
            track_results = sp.tracks(track_id_list)
            for track in track_results['tracks']:                              
                single_track_dict = {                                       
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'id': track['id'],
                    'release_date': track['album']['release_date'],
                    'popularity':  track['popularity'],
                }
                tracks_data_list.append(single_track_dict)
        except Exception as e:
            print(e)
            continue
    return tracks_data_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_data.py challenge_set.json")
    else:
        track_ids = list(get_track_ids(sys.argv[1]))
        tracks_data_list = get_tracks_data(track_ids, 50)
        audio_features_list = get_audio_features(track_ids , 100)

        tracks_data_df = pd.DataFrame(tracks_data_list)
        tracks_data_df.dropna(inplace=True)
        audio_features_df = pd.DataFrame(audio_features_list)
        audio_features_df.dropna(inplace=True)

        merged_df = tracks_data_df.merge(audio_features_df, on = 'id', how = 'left')
        merged_df.dropna(inplace=True)
        merged_df.to_csv('extracted_data.csv', sep = ',')
