#!/usr/bin/env python

import simplejson, random, itertools
from collections import defaultdict

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class HandEvents(object):

    def __init__(self):    
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce.png':2, 'three.png':3, 'four.png':4, 'five.png':5,
                      'six.png':6, 'seven.png':7, 'eight.png':8,'nine.png':9, 
                      'ten.png':10, 'jack.png':10, 'queen.png':10, 
                      'king.png':10, 'ace.png':11}
        self.deck = list(itertools.izip(self.suits, self.cards.keys() * 4)) * 6
        random.shuffle(self.deck)

    def deal_card(self):
        card = self.deck[0]
        self.deck.pop(0) 
        return card

    def total(self, cards):
        amount = 0
        for card in cards:
            if self.cards.has_key(card):
                amount += self.cards[card]
        if amount > 21 and 'ace' in cards:
            for i in range(cards.count('ace')):
                if amount > 21:
                    amount -= 10
        return amount

    def hold(self, score):
        comp = total(score)
        if comp > 16:
            return    
        if comp < 17:
            card = deck[0]
            deck.pop(0)
            return card


class Dealer(object):

    def __init__(self, players, seats):
        self.players = players
        self.seats = seats
        self.scores = dict()

    def new_hand(self):
        self.deal = HandEvents()  
        self.deal_players
        self.deal_dealer
        turn_msg = {'turn':min(self.players['players_list'])}
        turn_msg = simplejson.dumps(turn_msg)
        self.signal_players(turn_msg)

    @property
    def deal_players(self):
        hands = defaultdict(list)
        deal_hands = {'player_hands':hands}
        for player in self.players['players_list']:
            card1 = self.deal.deal_card()     
            card2 = self.deal.deal_card() 
            hand = [''.join(i for i in card1), ''.join(i for i in card2),
                    card1[1], card2[1]]
            for card in hand:
                deal_hands['player_hands'][player].append(card)
            self.scores[player] = self.deal.total(hand[2:])
        deal_hands = simplejson.dumps(deal_hands)
        score_msg = {'allscores':self.scores}
        score_msg = simplejson.dumps(score_msg)
        self.signal_players(deal_hands)
        self.signal_players(score_msg)

    @property
    def deal_dealer(self):
        card1 = self.deal.deal_card()
        hand = [''.join(i for i in card1), card1[1]]
        dealer_start = {'dealer_start':hand}
        dealer_start = simplejson.dumps(dealer_start)
        self.score = self.deal.total(hand[1:])
        dealer_score = {'dealer_score':self.score}
        dealer_score = simplejson.dumps(dealer_score)
        self.signal_players(dealer_start)
        self.signal_players(dealer_score)

    @property
    def dealer_take(self):
        card = self.deal.deal_card()
        dealer_card = {'dealer_card':[''.join(i for i in card), card[1]]}
        dealer_card = simplejson.dumps(dealer_card)
        self.score += self.deal.total(card[1:])
        dealer_score = {'dealer_score':self.score}
        dealer_score = simplejson.dumps(dealer_score)
        self.signal_players(dealer_card)
        self.signal_players(dealer_score)

    def score(self, player_stats):
        player = player_stats.keys()[0]
        score_msg = {'allscores':self.scores}
        score_msg = simplejson.dumps(score_msg)
        for player in self.seats:
            player.sendLine(score_msg)

    def dealers_turn(self):
        self.dealer_take
        if any(i < 22 for i in self.scores.values()):
            while self.score < 17:
                self.dealer_take

    def signal_players(self, msg):
        for player in self.seats:
            player.sendLine(msg)        


class GameData(LineReceiver):

    def __init__(self, dealer, players, clients): 
        self.players = players
        self.clients = clients 
        self.dealer = dealer
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
        print line
        game_msg = simplejson.loads(line)
        action = game_msg.keys()[0]
        if action == 'new_hand':  
            self.dealer.players = self.players
            self.dealer.seats = self.clients
            self.dealer.new_hand()
        elif action == 'player_total':
            self.dealer.score(game_msg['player_total'])
        elif action == 'dealers_turn':
            self.dealer.dealers_turn()
        else:
            game_msg = simplejson.dumps(game_msg)
            for client in self.clients:
                client.sendLine(game_msg)


class BlackFactory(Factory):

    def __init__(self):
        self.players = defaultdict(list)
        self.players['players_list']
        self.clients = dict() 
        self.dealer = Dealer(self.players, self.clients)

    def buildProtocol(self, addr):
        return GameData(self.dealer, self.players, self.clients) 


if __name__ == '__main__':
    reactor.listenTCP(6000, BlackFactory())
    reactor.run()
