#!/usr/bin/env python

import spotipy
import time
from pathlib import Path # I use this instead of os.path
from spotipy.oauth2 import SpotifyOAuth


# Path related
DIR_PATH   = Path(r'~/PolyPop/UIX/Sources/Spotify/')
TEMP_PATH  = Path(r'd:\spotify')
#CACHE_FILE = Path(r'{}/.cache'.format(DIR_PATH.expanduser()))
CACHE_FILE = Path(r'{}/.cache'.format(TEMP_PATH))


# Spotify Required
CLIENT_ID     = ''
CLIENT_SECRET = ''
SCOPE         = "user-read-playback-state,user-library-read,user-modify-playback-state,user-read-currently-playing"
REDIRECT_URI  = "http://localhost:38042"
CACHE_FILE_HANDLER = spotipy.cache_handler.CacheFileHandler(CACHE_FILE)


# "Globals"
CONNECT_STATE = False # Allowed: True | False
SHUFFLE_STATE = False # Allowed: True | False
REPEAT_STATE  = 'off' # Allowed: 'track' | 'context' | 'off'


# Volume Formatting
def volume_format(v):
    return float('%.2f' % v)


# Get devices, accepts Spotify object from create_spotify()
def get_devices(sp):
    return sp.devices().get('devices')


#----------------------------------------------------------------
# Start playback
# Requires: spotify and device_id objects
# Optional: song_uri, playlist_uri
def play(sp, dev_id, song_uri=None, playlist_uri=None):
    try:
        if playlist_uri:
            sp.start_playback(device_id=dev_id, context_uri=playlist_uri)
        if song_uri:
            sp.start_playback(device_id=dev_id, uris=[song_uri])
        if (song_uri == None and playlist_uri == None):
            sp.start_playback(device_id=dev_id)
        return
    except spotipy.SpotifyException as e:
        print(e)


# Pause Spotify, accepts Spotify object from create_spotify()
def pause(sp):
    try:
        sp.pause_playback()
    except spotipy.SpotifyException:
        pass


# Next Track, accepts Spotify object from create_spotify()
def next_track(sp):
    try:
        sp.next_track()
    except spotipy.SpotifyException:
        pass


# Previous Track, accepts Spotify object from create_spotify()
def previous_track(sp):
    try:
        sp.previous_track()
    except spotipy.SpotifyException:
        pass


#----------------------------------------------------------------
# Shuffle
# Accepts Spotify object from create_spotify(), device_id, state
def toggle_shuffle(sp,dev_id,state):
  # Supported States: True | False
    sp.shuffle(state, device_id=dev_id)


#----------------------------------------------------------------
# Repeat
# Accepts Spotify object from create_spotify(), device_id, state
def repeat(sp,dev_id,state):
  # Supported States: 'track' | 'context' | 'off'
    sp.repeat(state, dev_id)


# Adjust Volume
# Accepts Spotify object from create_spotify(), and volume integer
def volume(sp, vol):
    sp.volume(int(vol))


# See if target file exists, accepts Path() object
def file_exists(target_file):
    return Path(target_file).exists()


# Remove target file, accepts Path() object
def remove_file(doomed_file):
  # WARNING: This is permanent, no recovery possible
    return doomed_file.unlink()


# Create the connection and token for Spotify
# Returns Auth_manager, Spotify, and Token objects
def create_spotify():
    auth_manager = SpotifyOAuth(
        client_id     = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri  = REDIRECT_URI,
        scope         = SCOPE,
        cache_handler = CACHE_FILE_HANDLER
    )
    spotify = spotipy.Spotify(
        client_credentials_manager = auth_manager
    )
    auth_token = spotify.auth_manager.get_access_token()
    return auth_manager, spotify, auth_token


# Check token expiration, recreate if needed
# Accepts auth_manager, spotify, auth_token objects
# Returns these objects as well
def refresh_spotify(auth_manager, spotify, auth_token=None):
    if auth_token == None:
        auth_token = auth_manager.cache_handler.get_cached_token()
    if auth_manager.is_token_expired(auth_token):
        auth_manager, spotify, auth_token = create_spotify()
    return auth_manager, spotify, auth_token


# I tossed this together as a simple test, needs work
# It fails if Spotify is not currently playing
def get_now_playing(spotify):
    playing = spotify.currently_playing()
    if playing['is_playing']:
        artist_name = playing['item']['artists'][0]['name'] #Artist Name
        album_name  = playing['item']['album']['name'], #Album Name
        track_name  = playing['item']['name'], #Track Name
    else:
        artist_name, album_name, track_name = None, None, None
    return artist_name, album_name, track_name


if __name__ == '__main__':
    pass


'''

  # Basic usage for getting track info

if __name__ == '__main__':
    auth_manager, spotify, auth_token = create_spotify()
    while True:
        auth_manager, spotify, auth_token = refresh_spotify(auth_manager, spotify, auth_token)
        artist_name, album_name, track_name = get_now_playing(spotify)
        if track_name != None:
            print('Artist: {}, Album: {}, Track: {}'.format(
                artist_name, album_name, track_name)
            )
        else:
            print('Nothing is playing.')
        time.sleep(30)
'''