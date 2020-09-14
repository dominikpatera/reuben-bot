import json


class Channels():
    def __init__(self):
        self.channels = []
        self.loadChannels()

    def loadChannels(self):
        f = open(os.path.dirname(__file__) + '/../keys/channels.json', 'r')
        data = json.load(f)
        self.channels = data
        f.close()

    def getChannels(self):
        return self.channels
