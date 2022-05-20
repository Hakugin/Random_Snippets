#!/usr/bin/env python

#----------------------------------------------------------------
# Spotify Authentication Code rewrite for Jab's PolyPop plugin
# Work in progress, use with extreme caution
#----------------------------------------------------------------

import spotipy
from pathlib import Path # I use this instead of os.path
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler


# Path related
DIR_PATH   = Path(Path.home(),'PolyPop/UIX/Sources/Spotify/')
#CACHE_FILE = Path(DIR_PATH, '.cache-spotify')
TEMP_PATH  = Path(r'd:\spotify')
CACHE_FILE = Path(TEMP_PATH, '.cache-spotify')


# Spotify Required
CLIENT_ID     = ''
CLIENT_SECRET = ''
SCOPE         = "user-read-playback-state,user-library-read,user-modify-playback-state,user-read-currently-playing,playlist-read-private"
REDIRECT_URI  = "http://localhost:38042"

# Note: Added playlist-read-private to scope to retrieve private playlists


# "Globals"
#CONNECT_STATE = False # Allowed: True | False (Not implemented yet)
SHUFFLE_STATE = False # Allowed: True | False
REPEAT_STATE  = 'off' # Allowed: 'track' | 'context' | 'off'
CURRENT_VOL   = 25    # Set to an arbitrary low number


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
    success = False
    num_try = 1
    auth_manager = SpotifyOAuth(
        client_id     = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri  = REDIRECT_URI,
        scope         = SCOPE,
        cache_handler = CacheFileHandler(CACHE_FILE)
    )
    spotify = spotipy.Spotify(
        client_credentials_manager = auth_manager
    )
  # Try to obtain a token, delete .cache if it fails and try again
    while success is False:
        if num_try >= 3:
            print('Made {} attempts to authenticate. All failed'.format(num_try))
            #should replace with exception
            return spotify, {}
        try:
            auth_token = spotify.auth_manager.get_access_token()
            print('Success! Took {} attempts.'.format(num_try))
            success = True
        except spotipy.oauth2.SpotifyOauthError as e:
            if file_exists(CACHE_FILE):
                remove_file(CACHE_FILE)
            num_try += 1
            print(e)
    return spotify, auth_token


# Check token expiration, recreate if needed
# Accepts spotify, auth_token objects
# Returns these objects as well
def refresh_spotify(spotify, auth_token=None):
    auth_token = auth_token or spotify.auth_manager.cache_handler.get_cached_token()
    if spotify.auth_manager.is_token_expired(auth_token):
        spotify, auth_token = create_spotify()
    return spotify, auth_token


# Get the now playing cover art
def get_now_playing_art(sp):
    current_playback = sp.current_playback()
    if current_playback.get('context').get('type').lower() == 'playlist':
        playlist_id = str(current_playback.get('context').get('uri').split(':')[2])
        try:
            now_playing_art_url = sp.playlist_cover_image(
                '{}'.format(playlist_id))[0].get('url')
        except IndexError:
          # Should return location of "stock" art
            now_playing_art_url = None
    else:
        for image in current_playback.get('item').get('album').get('images'):
            if image.get('height') >= 640:
                now_playing_art_url = image.get('url')
    return now_playing_art_url


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


'''

  # Basic usage for getting track info

if __name__ == '__main__':
    spotify, auth_token = create_spotify()
    while True:
        spotify, auth_token = refresh_spotify(spotify, auth_token)
        artist_name, album_name, track_name = get_now_playing(spotify)
        if track_name != None:
            print('Artist: {}, Album: {}, Track: {}'.format(
                artist_name, album_name, track_name)
            )
        else:
            print('Nothing is playing.')
        time.sleep(30)
'''
