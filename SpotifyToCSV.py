import requests
import csv

# Set up the authentication parameters for Spotify
client_id = 'yourspotifyID'
client_secret = 'yourspotifysecret'
spotify_auth_url = 'https://accounts.spotify.com/api/token'
spotify_auth_response = requests.post(spotify_auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})
spotify_access_token = spotify_auth_response.json()['access_token']

# Set up the authentication parameters for Apple Music
music_kit_id = 'yourmusickitID'
music_kit_secret = 'yourmusickitsecret'
apple_music_auth_url = 'https://appleid.apple.com/auth/oauth2/token'
apple_music_auth_response = requests.post(apple_music_auth_url, {
    'grant_type': 'client_credentials',
    'client_id': music_kit_id,
    'client_secret': music_kit_secret,
})
apple_music_access_token = apple_music_auth_response.json()['access_token']

# Set up the request parameters for Spotify
spotify_headers = {
    'Authorization': 'Bearer ' + spotify_access_token
}
spotify_limit = 9999
spotify_offset = 0

# Set up the request parameters for Apple Music
apple_music_headers = {
    'Authorization': 'Bearer ' + apple_music_access_token,
    'Music-User-Token': 'your_music_user_token', # Replace with your own Music User Token
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
apple_music_url = 'https://api.music.apple.com/v1/me/library'

# Retrieve the metadata from the Spotify library
spotify_url = 'https://api.spotify.com/v1/me/tracks?limit={}&offset={}'.format(spotify_limit, spotify_offset)
response = requests.get(spotify_url, headers=spotify_headers)
data = response.json()

# Format the metadata as a CSV file
rows = []
for item in data['items']:
    track = item['track']
    artist = ', '.join([a['name'] for a in track['artists']])
    album = track['album']['name']
    release_date = track['album']['release_date']
    duration_ms = track['duration_ms']
    popularity = track['popularity']
    rows.append([artist, track['name'], album, release_date, duration_ms, popularity])

# Save the CSV file to disk
with open('spotify_library.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Artist', 'Track', 'Album', 'Release Date', 'Duration (ms)', 'Popularity'])
    writer.writerows(rows)

# Read the CSV file and add each song to the Apple Music library
with open('spotify_library.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        artist, track_name, album_name, release_date, duration_ms, popularity = row
        search_url = 'https://api.music.apple.com/v1/catalog/us/search'
        search_response = requests.get(search_url, headers=apple_music_headers, params={
            'term': track_name + ' ' + artist,
            'types': 'songs',
            'limit': 1,
        })
        search_data = search_response.json()
        if 'results' in search_data and 'songs' in search_data['results']:
            song_id = search_data['results']['songs']['data'][0]['
