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
    return render_template('connect.html')

# POST /connect
# try to connect
@app.route('/connect', methods=['POST'])
def connect():
    # get information given by user
    user_id = request.form.get('UserID')
    client_id = request.form.get('ClientID')
    client_secret = request.form.get('ClientSecret')

    global cli
    cli = Client(client_id, client_secret, user_id)
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
    data = { "title" : "Saved Songs"}
    return render_template('songs.html', data=data)

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
    return render_template('songs.html', data=data)

# GET /actions/top_songs
@app.route('/actions/top_songs', methods=['GET'])
def my_top_songs():
    global cli
    data = cli.get_my_top_tracks()
    return render_template('songs.html', data=data) 

# GET /actions/recent
@app.route('/actions/recent', methods=['GET'])
def my_last_played_songs():
    global cli
    try:
        data = cli.get_last_played_tracks()
    except:
        cli.refresh_token()
        data = cli.get_last_played_tracks()
    return render_template('songs.html', data=data)

# GET /actions/search//song/{name}
@app.route('/actions/search/song/<name>', methods=['GET'])
def search_song(name):
    global cli
    data = cli.search_for_song(name)
    return render_template('songs.html', data=data)

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
        return render_template('songs.html', data=data)
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
    return render_template('songs.html', data=data)

if __name__ == ' __main__':
    app.debug = True
    app.run()