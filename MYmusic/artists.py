
class Artists:
    def __init__(self, title):
        self.title = title
        self.artists = {}
    
    def add_artist(self, artist_id, artist_name, popularity, genres):
        self.artists[artist_id] = {
            "artist" : artist_name,
            "popularity" : popularity,
            "genres" : genres
            }
    def remove_artist(self, id):
        self.artists.remove(id)
    
