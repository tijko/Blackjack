#!/usr/bin/env python
#
import time
#
import simplejson
import random
from collections import defaultdict

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class Dealer(object):

    def __init__(self, players, seats):
        self.players = players
        self.seats = seats
        self.scores = dict()

    def new_hand(self):
        players = simplejson.dumps(self.players) 
        self.signal_players(players)
        self.deal = HandEvents()  
        self.player_blackjacks = 0
        self.deal_players
        self.deal_dealer
        turn = min(self.players['players_list'])        
        turn_msg = {'turn':turn}
        turn_msg = simplejson.dumps(turn_msg)
        self.signal_players(turn_msg)

    def deal_card(self, player): 
        if self.scores:
            card = self.deal.deal_card()
            self.hands[player].append(card[1])
            player_hand = self.hands[player]
            self.scores[player] = self.deal.total(player_hand)
            card_msg = {'player_card':{player:card}}
            card_msg = simplejson.dumps(card_msg)
            self.signal_players(card_msg)        
            self.send_player_score(player)

    @property
    def deal_players(self):
        self.hands = defaultdict(list)
        deal_hands = {'player_hands':defaultdict(list)}
        for player in self.players['players_list']:
            card1 = self.deal.deal_card()     
            card2 = self.deal.deal_card() 
            hand = [''.join(card1), ''.join(card2),
                    card1[1], card2[1]]
            self.hands[player] = [card1[1], card2[1]]
            for card in hand[:2]: 
                deal_hands['player_hands'][player].append(card)
            self.scores[player] = self.deal.total(hand[2:]) 
            if self.scores[player] == 21:
                self.player_blackjacks += 1
            self.send_player_score(player)
        deal_hands = simplejson.dumps(deal_hands)
        self.signal_players(deal_hands)

    @property
    def deal_dealer(self):
        card1 = self.deal.deal_card()
        hand = [''.join(card1), card1[1]]
        self.hand = list(card1[1:])
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
        self.hand.append(card[1])
        dealer_card = {'dealer_card':[''.join(card), card[1]]}
        dealer_card = simplejson.dumps(dealer_card)
        self.score = self.deal.total(self.hand)
        if len(self.hand) == 2 and self.score == 21:
            dealer_score = {'dealer_score':'Blackjack'}
        else:
            dealer_score = {'dealer_score':self.score}
        dealer_score = simplejson.dumps(dealer_score)
        self.signal_players(dealer_card)
        self.signal_players(dealer_score)

    def send_player_score(self, player):
        player_seats = {v:k for k,v in self.seats.items()}
        score_msg = {'score':self.scores[player]}
        score_msg = simplejson.dumps(score_msg)
        player_seats[player].sendLine(score_msg.encode("utf-8"))

    def dealers_turn(self):
        if self.scores:
            self.dealer_take  
            players_in = [i for i in self.scores.values() if i < 22]
            if players_in and self.player_blackjacks < len(players_in):
                while self.score < 17:
                    self.dealer_take
            results_msg = {'results':None}
            results_msg = simplejson.dumps(results_msg)
            self.signal_players(results_msg)
            self.scores = dict()

    def signal_players(self, msg):
        for player in self.seats:
            player.sendLine(msg.encode("utf-8"))        


class HandEvents(object):

    def __init__(self):    
        self.suits = ['heart', 'diamond', 'spade', 'club'] * 13
        self.cards = {'deuce.png':2, 'three.png':3, 'four.png':4, 'five.png':5,
                      'six.png':6, 'seven.png':7, 'eight.png':8, 'nine.png':9, 
                      'ten.png':10, 'jack.png':10, 'queen.png':10, 
                      'king.png':10, 'ace.png':11}
        self.deck = list(zip(self.suits, list(self.cards.keys()) * 4)) * 6
        random.shuffle(self.deck)

    def deal_card(self):
        card = self.deck.pop(0)
        return card

    def total(self, cards):
        amount = 0
        for card in cards:
            if card in self.cards:
                amount += self.cards[card]
        if amount > 21 and 'ace.png' in cards: 
            for i in range(cards.count('ace.png')): 
                if amount > 21:
                    amount -= 10
        return amount


class GameData(LineReceiver):

    def __init__(self, dealer, players, clients, game): 
        self.players = players
        self.clients = clients 
        self.dealer = dealer
        self.next_game = game
        self.max_players = set(range(1, 5)) 

    def connectionMade(self):
        if len(self.players['players_list']) <= 3:
            taken_seats = self.next_game.values()
            available_seats = self.max_players.difference(taken_seats)
            new_player = list(available_seats)[0]
            self.next_game[self] = new_player
            if not self.players['players_list']:
                self.clients[self] = new_player
                self.players['players_list'].append(new_player)
                updated_players = simplejson.dumps(self.players)
                for client in self.clients:
                    client.sendLine(updated_players.encode("utf-8"))
        else:
            table_full = {'table_full':None} 
            msg = simplejson.dumps(table_full)
            self.sendLine(msg.encode("utf-8"))

    def connectionLost(self, reason):
        print("Player {} disconnected!".format(self))
        if self in self.clients:
            lost_player = self.clients[self]
            self.players['players_list'].remove(lost_player)
            del self.clients[self]
            self.dealer.seats = self.clients
        del self.next_game[self]
        updated_players = simplejson.dumps(self.players)
        for client in self.clients:
            client.sendLine(updated_players.encode("utf-8"))

    def lineReceived(self, line):
        game_msg = simplejson.loads(line)
        action = list(game_msg.keys())[0]
        if action == 'new_hand':  
            for k in self.next_game:
                if k not in self.clients:
                    self.clients[k] = self.next_game[k]
                    self.players['players_list'].append(self.next_game[k])
                    players_msg = simplejson.dumps(self.players)
                    k.sendLine(players_msg.encode("utf-8"))
            self.dealer.players = self.players
            self.dealer.seats = self.clients
            self.dealer.new_hand()
        elif action == 'dealers_turn':
            self.dealer.dealers_turn()
        elif action == 'player_card':
            self.dealer.deal_card(game_msg['player_card'])
        else:
            game_msg = simplejson.dumps(game_msg)
            for client in self.clients:
                client.sendLine(game_msg.encode("utf-8"))


class BlackFactory(Factory):

    def __init__(self):
        self.players = defaultdict(list)
        self.players['players_list']
        self.clients = dict() 
        self.game = dict()
        self.dealer = Dealer(self.players, self.clients)

    def buildProtocol(self, addr):
        return GameData(self.dealer, 
                        self.players, 
                        self.clients, 
                        self.game) 


if __name__ == '__main__':
    reactor.listenTCP(6000, BlackFactory())
    reactor.run()
