#!/usr/bin/env python

import simplejson
import sys
import os

import pygame

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall

from lib.graphics_ctrl import GameDisplay


class Client(object):
    """
    Class to handle setting default screen, to check data received from the server,
    send data to the server, and handle pygame events.
    """
    def __init__(self):
        self.turn = 0
        self.player = None
        self.deal_lock = False 
        self.dealer_bj = False
        self.player_bj = False
        self.gd = GameDisplay()
        self.gd.default_scr()
        self.msg_actions = {'table_full':self.table_full,
                            'players_list':self.players,
                            'player_card':self.player_card,
                            'player_hands':self.player_hands,
                            'dealer_start':self.dealer_hand,
                            'dealer_score':self.dealer_score,
                            'dealer_card':self.dealer_card,
                            'turn':self.player_turn,
                            'allscores':self.table_totals
                           } 
        reactor.callLater(0.1, self.tick) # switch between pygame and twisted signals

    def game_messages(self, msg): 
        print msg
        game_msg = simplejson.loads(msg)
        msg_type = game_msg.keys()[0]
        load = game_msg[msg_type]
        self.msg_actions[msg_type](load)

    def players(self, player_list): 
        if not self.player:
            self.player = player_list[-1]
            self.pl_key = str(self.player)
        self.playrlst = player_list

    def player_turn(self, turn):
        if turn == self.player:
            self.turn = turn
            if self.player_score == 21:
                self.turn += 1
                turn_msg = {'turn':self.turn}
                turn_msg = simplejson.dumps(turn_msg)
                self.player_bj = True
                self.allscores[self.player] = 'Blackjack'
                score_msg = simplejson.dumps(self.allscores)
                self.sendLine(score_msg)
                self.sendLine(turn_msg)
        elif turn > len(self.playrlst) and self.player == 1:
            dealer_msg = {'dealers_turn':None}
            dealer_msg = simplejson.dumps(dealer_msg)
            self.sendLine(dealer_msg)

    def player_hands(self, hands):
        self.gd.default_scr()
        self.deal_lock = True 
        self.hand_values = hands[self.pl_key][2:] 
        self.player_hand = hands[self.pl_key][:2]
        hands = [hand[:2] for hand in hands.values()]
        self.gd.display_hands(hands)

# HIT / Take a card method
    def player_card(self, msg): 
        if msg[0] == self.player:
            self.gd.display_card(msg[2], self.player)
            self.player_score.append(msg[3])
            self.player_amount = total(self.player_score)
            self.player_hand.append(msg[2])
            if self.player_amount > 21:
                self.player_bust()
        if msg[0] != self.player:
            self.gd.display_card(msg[0], msg[1])

    def player_bust(self):
        self.turn += 1
        turn_msg = {'turn':self.turn}
        turn_msg = simplejson.dumps(turn_msg)
        self.allscores[self.player] = self.player_amount
        score_msg = simplejson.dumps(self.allscores)
        self.sendLine(score_msg)
        self.sendLine(turn_msg)
        self.gd.player_bust()

    @property
    def player_total(self):
        total_msg = {'player_total':{self.player:self.hand_values}}
        total_msg = simplejson.dumps(total_msg)
        self.sendLine(total_msg)         
        
    def table_totals(self, scores):
        self.allscores = scores
        self.player_score = scores[self.pl_key] 

    def dealer_hand(self, hand):
        self.gd.display_dealer(hand[0])
        self.dealer_hand = [hand[0]]

    def dealer_score(self, score):
        self.dealer_score = score

    def dealer_card(self, card):
        self.dealer_hand.append(card[1])
        self.gd.display_dealer_take(card)

    def results(self):
        if self.dealer_bj and not self.player_bj:	
            self.gd.dealer_bj()
        elif self.player_bj and not self.dealer_bj:
            self.gd.player_bj()
        elif self.dealer_amount > self.player_amount:
            self.gd.dealer_win()
        elif self.dealer_amount == self.player_amount:
            self.gd.tie()
        elif self.dealer_amount < self.player_amount:
            self.gd.player_win()
               
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                reactor.stop()
                self.gd.exit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # gets mouse coordinates if mouse clicked 
                pos = pygame.mouse.get_pos()
                if self.gd.stand.collidepoint(pos) and self.player == self.turn:
                    self.turn += 1
                    self.allscores[self.player] = self.player_score
                    turn_msg = {'turn':self.turn}
                    turn_msg = simplejson.dumps(turn_msg)
                    score_msg = {'allscores':self.allscores}
                    score_msg = simplejson.dumps(score_msg)
                    self.sendLine(score_msg)
                    self.sendLine(turn_msg)
                if self.gd.deal.collidepoint(pos) and self.deal_lock == False:
                    deal_msg = {'new_hand':None}
                    deal_msg = simplejson.dumps(deal_msg)
                    self.sendLine(deal_msg)                    
                    self.deal_lock = True
                if (self.gd.hit.collidepoint(pos) and 
                    self.player_total < 21 and 
                    self.turn == self.player):
#                    new_card = Take().card()    
                    card = ['card', self.player, 
                            new_card[0] + new_card[1] + '.png',
                            new_card[1]]
                    card = simplejson.dumps(card)
                    self.sendLine(card)

    def table_full(self, msg):
        reactor.stop()
        self.gd.exit()
        print "Table Full"


class BlackClientProtocol(LineReceiver):
    """ 
    Class client for receiving data from the server.
    """
    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self, line):
        self.recv(line)


class BlackClient(ClientFactory):
    """
    Class that builds protocol instances.
    """
    def __init__(self, client):
        self.client = client

    # builds protocol instance  
    def buildProtocol(self, addr):
        proto = BlackClientProtocol(self.client.game_messages)
        self.client.sendLine = proto.sendLine
        return proto


if __name__ == '__main__':
    c = Client()
    # LoopingCall method to keep checking 'tick' method for pygame events 
    lc = LoopingCall(c.tick)
    lc.start(0.1)
    reactor.connectTCP('192.168.1.3', 6000, BlackClient(c))
    reactor.run()
