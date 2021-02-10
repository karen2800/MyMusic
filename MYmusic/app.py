from flask import Flask, jsonify, json, render_template, request, redirect
import os, ast 
from client import Client
import urllib.parse

app = Flask(__name__)

global cli

# GET /
# getting started -- LOGIN
@app.route('/', methods=['GET'])
def main():
    client_id = os.getenv('client_id') 
    client_secret = os.getenv('client_secret')

    global cli
    cli = Client(client_id, client_secret)
    response = cli.get_code()

    return render_template('next.html', response=response)

# callback -- get code
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    query = str(request.query_string).replace("'", "")
    code = query.split("&")[0]
    state = query.split("&")[1]
    code = code.split("=")[1]
    state = state.split("=")[1]

    return redirect(f'/callback/{code}')

# GET /callback/code
# get code
@app.route('/callback/<code>', methods=['GET'])
def got_code(code):
    # get token
    global cli
    cli.first_token(code)
    # connected
    return redirect('/actions')

# GET /actions
# main page
@app.route('/actions', methods=['GET', 'POST'])
def actions():
    return render_template('index.html')

# GET /actions/saved
@app.route('/actions/saved', methods=['GET'])
def saved_songs():
    global cli
    data = cli.saved_songs
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved)

# POST /actions/saving
@app.route('/actions/saving', methods=['POST'])
def saved_songs_saving():
    global cli
    song_id = request.form.get('song_id')
    artist = request.form.get('artist')
    title = request.form.get('title')

    song = {
        "artist" : artist,
        "title" : title
    }
    song_added = False

    if cli.saved_songs.songs.get(song_id) is None:
        # add song
        cli.add_to_saved_songs(song_id, song)
        song_added = True
    else:
        # remove song
        cli.remove_from_saved_songs(song_id)

    return jsonify({'result' : 'success', 'song_added' : song_added })

# GET /actions/search
@app.route('/actions/search', methods=['GET'])
def search():
    data = { "title" : "Search"}
    return render_template('search.html', data=data)

# GET /actions/top_artists
@app.route('/actions/top_artists', methods=['GET'])
def top_artists():
    global cli
    data = cli.get_my_top_artists()
    return render_template('top_artists.html', data=data) 

# POST /actions/top_artists
@app.route('/actions/top_artists', methods=['POST'])
def top_artist_songs():
    global cli
    artist_id = request.form.get('artist_id')
    data = cli.get_artist_top_tracks(artist_id)
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved)

# GET /actions/top_songs
@app.route('/actions/top_songs', methods=['GET'])
def my_top_songs():
    global cli
    data = cli.get_my_top_tracks()
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved) 

# GET /actions/recent
@app.route('/actions/recent', methods=['GET'])
def my_last_played_songs():
    global cli
    try:
        data = cli.get_last_played_tracks()
    except:
        cli.refresh_token()
        data = cli.get_last_played_tracks()
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved)

# GET /actions/search//song/{name}
@app.route('/actions/search/song/<name>', methods=['GET'])
def search_song(name):
    global cli
    data = cli.search_for_song(name)
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved)

# GET /actions/search
@app.route('/actions/search', methods=['POST'])
def search_item():
    global cli
    search_item = request.form.get('search_item')
    search_type = request.form.get('search_type')

    # search for song
    if search_type == "song":
        try:
            data = cli.search_for_song(search_item)
        except:
            cli.refresh_token()
            data = cli.search_for_song(search_item)
        saved = cli.saved_songs.get_id_list()
        return render_template('songs.html', data=data, saved=saved)
    # search for artist
    else:
        try:
            data = cli.search_for_artist(search_item)
        except:
            cli.refresh_token()
            data = cli.search_for_artist(search_item)
        return render_template('top_artists.html', data=data)

# GET /actions/search/artist/{name}
@app.route('/actions/search/artist/<name>', methods=['GET'])
def search_artist(name):
    global cli
    try:
        data = cli.search_for_artist(name)
    except:
        cli.refresh_token()
        data = cli.search_for_artist(name)
    return render_template('top_artists.html', data=data)

# GET /actions/playlists
@app.route('/actions/playlists', methods=['GET'])
def my_playlists():
    global cli
    try:
        data = cli.get_my_playlists()
    except:
        cli.refresh_token()
        data = cli.get_my_playlists()
    return render_template('playlists.html', data=data)

# POST /actions/playlists
@app.route('/actions/playlists', methods=['POST'])
def playlist_songs():
    global cli
    playlist_id = request.form.get('playlist_id')
    try:
        data = cli.get_my_playlist_data(playlist_id)
    except:
        cli.refresh_token()
        data = cli.get_my_playlist_data(playlist_id)
    saved = cli.saved_songs.get_id_list()
    return render_template('songs.html', data=data, saved=saved)

if __name__ == ' __main__':
    app.debug = True
    app.run()