
class Songs:
    def __init__(self, title):
        self.title = title
        self.songs = {}
        self.attributes = {}
        self.attr_avgs = {}
    
    def add_song(self, id, song):
        self.songs[id] = song
    def remove_song(self, id):
        self.songs.pop(id)

    def add_attributes(self, id, attributes):
        self.songs[id]["attributes"] = attributes
        for k, v in attributes.items():
            if self.attributes is None or k not in self.attributes.keys():
                self.attributes[k] = v
            else:
                self.attributes[k] += v

    def calc_attr_avg(self):
        avgs = {}
        for k, v in self.attributes.items():
            avgs[k] = round(v / len(self.songs), 3)
        self.attr_avgs = avgs

    
