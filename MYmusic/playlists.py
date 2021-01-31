from playlist import Playlist

class Playlists:
    def __init__(self):
        self.title = "My Playlists"
        self.playlists = {}
    
    def add_playlist(self, id, playlist):
        self.playlists[id] = playlist
    def remove_playlist(self, id):
        self.playlists.pop(id)