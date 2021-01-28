class Playlist:
    def __init__(self):
        self.name = "NEW playlist"
        self.id = None
        self.songs = {}

    # add or update
    def add_song(self, song):
        self.songs[song.id] = { "name" : song.name }

    def add_songs(self, songs):
        for song in songs:
            self.add_song(song)

    # remove
    def remove_song(self, id):
        self.songs.pop(id)

    def remove_songs(self, ids):
        for id in ids:
            self.songs.pop(id)
