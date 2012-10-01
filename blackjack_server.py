import simplejson

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Game_Data(LineReceiver):
    def __init__(self, players, clients): 
        self.players = players
        self.clients = clients 

    def connectionMade(self):
        new_player = 'player_' + str(len(self.players) + 1)
        self.clients.append(self)
        self.players.append(new_player)
        self.players = simplejson.dumps(self.players)
        for client in self.clients:
            client.sendLine(self.players)

    def lineReceived(self,line):
        self.line = line
        print self.line
        for client in self.clients:
            client.sendLine(self.line)


class BlackFactory(Factory):
    def __init__(self):
        self.players = []
        self.clients = []

    def buildProtocol(self, addr):
        return Game_Data(self.players, self.clients) 


reactor.listenTCP(6000, BlackFactory())
reactor.run()

