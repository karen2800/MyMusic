
import statistics

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
    def get_ids(self):
        keys = ""
        for k, v in self.songs.items():
            keys += k + ","
        return keys[:-1]
    def get_id_list(self):
        ids = self.get_ids().split(",")
        return ids

    def add_attributes(self, id, attributes):
        self.songs[id]["attributes"] = attributes
        for k, v in attributes.items():
            if self.attributes is None or k not in self.attributes.keys():
                if k == "key":
                    self.attributes[k] = []
                    self.attributes[k].append(v)
                else:
                    self.attributes[k] = v
            else:
                if k == "key":
                    self.attributes[k].append(v)
                else:
                    self.attributes[k] += v

    def calc_attr_avg(self):
        avgs = {}
        for k, v in self.attributes.items():
            if k == "key":
                avgs[k] = statistics.mode(v)
            else:   
                avgs[k] = round(v / len(self.songs), 3)
        self.attr_avgs = avgs

    
