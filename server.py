#!/usr/bin/env python

import simplejson

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class Game_Data(LineReceiver):

    def __init__(self, players, clients): 
        self.players = players
        self.clients = clients 

    def connectionMade(self):
        if len(self.players) <= 3:
            new_player = 'player_' + str(len(self.players[1:]) + 1)
            self.clients[self] = new_player
            self.players.append(new_player)
            updated_players = simplejson.dumps(self.players)
            for client in self.clients:
                client.sendLine(updated_players)
        else:
            table_full = simplejson.dumps("Table Full")
            self.sendLine(table_full)

    def connectionLost(self, reason):
        print "Player %s disconnected!" % self
        lost_player = self.clients[self]
        self.players.remove(lost_player)
        del self.clients[self]
        updated_players = simplejson.dumps(self.players)
        for client in self.clients:
            client.sendLine(updated_players)

    def lineReceived(self, line):
        self.line = line
        for client in self.clients:
            client.sendLine(self.line)


class BlackFactory(Factory):

    def __init__(self):
        self.players = ['players_list']
        self.clients = dict() 

    def buildProtocol(self, addr):
        return Game_Data(self.players, self.clients) 


if __name__ == '__main__':
    reactor.listenTCP(6000, BlackFactory())
    reactor.run()

