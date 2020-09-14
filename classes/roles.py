import json
import os


class Roles:
    def __init__(self):
        self.mainR = []
        self.interests = []
        self.games = []
        self.loadRoles()

    def loadRoles(self):
        f = open(os.path.dirname(__file__) + '/../keys/roles.json', 'r')
        data = json.load(f)
        self.mainR = data['main']
        self.interests = data['interests']
        self.games = data['games']
        f.close()

    def getMainRoles(self):
        return self.mainR

    def getInterestsRoles(self):
        return self.interests

    def getGamesRoles(self):
        return self.games
