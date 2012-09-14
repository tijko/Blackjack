from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import simplejson

class Chat(LineReceiver):
    def __init__(self, users, players):
        self.users = users
        self.name = None
        self.players = players

    def connectionMade(self):
        new = 'player_' + str(len(self.players) + 1)
        self.players.append(new)
        self.jason = self.players
        self.jason = simplejson.dumps(self.jason) 
        self.sendLine(self.jason)

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}  
        self.players = []

    def buildProtocol(self, addr):
        return Chat(self.users,self.players)


reactor.listenTCP(6000, ChatFactory())
reactor.run()

