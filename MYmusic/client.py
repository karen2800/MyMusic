import requests, json, base64, ast
from myToken import Token
from playlist import Playlist
from playlists import Playlists
from songs import Songs
from artists import Artists

class Client:
    def __init__(self, client_id, client_secret, user_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.token = None
        self.saved_songs = Playlist()

    # add songs to saved songs playlist
    def add_to_saved_songs(self, songs):
        # k: song id
        # v: song { "artist" : "", "title": ""}
        for k, v in songs:
            self.saved_songs.songs.add_song(k, v)

    # get user playlists
    def get_my_playlists(self):
        url = "https://api.spotify.com/v1/me/playlists"
        response = self.get_request(url)
        response_json = response.json()

        playlists = Playlists()
        for p in response_json["items"]:
            playlist = Playlist(p["name"], p["id"])
            playlists.add_playlist(p["id"], playlist)

        return playlists

    # get user playlist
    def get_my_playlist_data(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = self.get_request(url)
        response_json = response.json()

        ids = ""
        tracks = Songs(response_json["name"])
        for track in response_json["tracks"]["items"]:
            ids = ids + track["track"]["id"] + "," 
            song = {
                "artist" : track["track"]["artists"][0]["name"],
                "title" : track["track"]["name"]
            }
            tracks.add_song(track["track"]["id"], song)

        return self.get_track_data(ids[:-1], tracks)

    # search for artist
    def search_for_artist(self, name):
        nameFormatted = name.replace(" ", "+")
        url = f"https://api.spotify.com/v1/search?q={nameFormatted}&type=artist"
        response = self.get_request(url)
        response_json = response.json()

        data = Artists(name)

        for artist in response_json["artists"]["items"]:
            genres = ', '.join([str(elem) for elem in artist["genres"]]) 
            data.add_artist(artist["id"], artist["name"], artist["popularity"], genres)

        return data

    # search for song
    def search_for_song(self, name):
        nameFormatted = name.replace(" ", "+")
        url = f"https://api.spotify.com/v1/search?q={nameFormatted}&type=track&market=US"
        response = self.get_request(url)
        response_json = response.json()

        ids = ""
        tracks = Songs(name)
        for track in response_json["tracks"]["items"]:
            ids = ids + track["id"] + "," 
            song = {
                "artist" : track["artists"][0]["name"],
                "title" : track["name"]
            }
            tracks.add_song(track["id"], song)

        return self.get_track_data(ids[:-1], tracks)

    # get last played tracks
    def get_last_played_tracks(self, limit=20):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self.get_request(url)
        response_json = response.json()

        ids = ""
        tracks = Songs("My Last Played Songs")
        for track in response_json["items"]:
            ids = ids + track["track"]["id"] + "," 
            song = {
                "artist" : track["track"]["artists"][0]["name"],
                "title" : track["track"]["name"]
            }
            tracks.add_song(track["track"]["id"], song)

        return self.get_track_data(ids[:-1], tracks)

    # my top tracks
    def get_my_top_tracks(self):
        url = "https://api.spotify.com/v1/me/top/tracks"
        response = self.get_request(url)
        response_json = response.json()

        ids = ""
        tracks = Songs("My Top Songs")
        for track in response_json["items"]:
            ids = ids + track["id"] + "," 
            song = {
                "artist" : track["artists"][0]["name"],
                "title" : track["name"]
            }
            tracks.add_song(track["id"], song)

        return self.get_track_data(ids[:-1], tracks)

    # get my top artists
    def get_my_top_artists(self):
        url = "https://api.spotify.com/v1/me/top/artists"
        response = self.get_request(url)
        response_json = response.json()

        data = Artists("My Top Artists")

        for artist in response_json["items"]:
            genres = ', '.join([str(elem) for elem in artist["genres"]]) 
            data.add_artist(artist["id"], artist["name"], artist["popularity"], genres)

        return data

    def get_artist_top_tracks(self, id):
        url = f"https://api.spotify.com/v1/artists/{id}/top-tracks?country=US"
        response = self.get_request(url)
        response_json = response.json()

        ids = ""
        data = Songs(response_json["tracks"][0]["artists"][0]["name"])

        for track in response_json["tracks"]:
            ids = ids + track["id"] + ","   
            song = { 
                "artist" : track["artists"][0]["name"],
                "title" : track["name"]
            }
            data.add_song(track["id"], song)

        return self.get_track_data(ids[:-1], data)

    # get ALL track data
    def get_track_data(self, ids, data):
        url = f"https://api.spotify.com/v1/audio-features/?ids={ids}"
        res = self.get_request(url)
        res_json = res.json()

        id_list = ids.split(",")
        audio_features = ["valence", "tempo", "energy", "acousticness", "key"]
        
        if len(id_list) > 0 and res_json["audio_features"] != None and len(res_json["audio_features"]) > 0:
            count = 0
            for track in res_json["audio_features"]:
                attributes = {}
                if track is not None:
                    for feature in audio_features:
                        attributes[feature] = track[feature]
                    data.add_attributes(id_list[count], attributes)
                    count = count + 1

            data.calc_attr_avg()

        return data

    def get_header(self):
        msg = f"{self.client_id}:{self.client_secret}"
        msg_bytes = msg.encode("ascii")
        base64_bytes = base64.b64encode(msg_bytes)
        base64_msg = base64_bytes.decode("ascii")
        return "Basic " + base64_msg

    # Get request
    def get_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token.access}"
            }
        )
        return response

    # Post request
    def post_request(self, url, data, header=None):
        if header == None:
            response = requests.post(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token.access}"
                }
            )
        else:
            response = requests.post(
                url, 
                headers=header, 
                data=data
            )
        return response

    def refresh_token(self):
        authTokenUrl = "https://accounts.spotify.com/api/token"
        authHeader = {}
        authData = {}

        authHeader["Authorization"] = self.get_header()
        authData["grant_type"] = "refresh_token"
        authData["refresh_token"] = self.token.refresh

        response = self.post_request(authTokenUrl, authData, authHeader)
        response_json = response.json()
        self.token.access = response_json["access_token"]

    def first_token(self, code):
        authTokenUrl = "https://accounts.spotify.com/api/token"
        authHeader = {}
        authData = {}

        authHeader["Authorization"] = self.get_header()
        authData["grant_type"] = "authorization_code" 
        authData["code"] = code
        authData["redirect_uri"] = "http://127.0.0.1:5000/callback"

        response = self.post_request(authTokenUrl, authData, authHeader)
        response_json = response.json()

        self.token = Token(response_json["access_token"], response_json["refresh_token"])
    
    # get code
    def get_code(self):
        scopes = []
        # users
        scopes.append("user-read-email")
        scopes.append("user-read-private")
        # library
        scopes.append("user-library-modify")
        scopes.append("user-library-read")
        # listening history
        scopes.append("user-read-recently-played")
        scopes.append("user-read-playback-position")
        scopes.append("user-top-read")
        # playlists
        scopes.append("playlist-modify-private")
        scopes.append("playlist-read-collaborative")
        scopes.append("playlist-read-private")
        scopes.append("playlist-modify-public")
        # playback
        scopes.append("streaming")
        scopes.append("app-remote-control")

        my_scopes = ""
        for index, s in enumerate(scopes):
            my_scopes += s
            if index < len(scopes) - 1:
                my_scopes += "%20"

        response = {}
        response["url"] = 'https://accounts.spotify.com/authorize'
        response["client_id"] = self.client_id
        response["redirect_uri"] = 'http://127.0.0.1:5000/callback'
        response["scope"] = my_scopes
        response["state"] = "5djek9"
        response["response_type"] = "code"

        return response