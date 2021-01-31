from songs import Songs

class Playlist:
    def __init__(self, name=None, id=None):
        # playlist name
        if name == None:
            self.name = "NEW playlist"
        else:
            self.name = name

        # playlist id
        if id == None:
            self.id = None
        else:
            self.id = id

        # songs
        self.songs = Songs(self.name)
