#!/usr/bin/env python

import simplejson
from collections import defaultdict

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class Game_Data(LineReceiver):

    def __init__(self, players, clients): 
        self.players = players
        self.clients = clients 
        self.max_players = set(range(1, 4))

    def connectionMade(self):
        if len(self.players['players_list']) <= 3:
            taken_seats = self.players['players_list']
            available_seats = list(self.max_players.difference(taken_seats))
            new_player = available_seats[0]
            self.clients[self] = new_player
            self.players['players_list'].append(new_player)
            updated_players = simplejson.dumps(self.players)
            for client in self.clients:
                client.sendLine(updated_players)
        else:
            table_full = {'table_full':None} 
            msg = simplejson.dumps(table_full)
            self.sendLine(msg)

    def connectionLost(self, reason):
        print "Player %s disconnected!" % self
        lost_player = self.clients[self]
        self.players['players_list'].remove(lost_player)
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
        self.players = defaultdict(list)
        self.players['players_list']
        self.clients = dict() 

    def buildProtocol(self, addr):
        return Game_Data(self.players, self.clients) 


if __name__ == '__main__':
    reactor.listenTCP(6000, BlackFactory())
    reactor.run()

