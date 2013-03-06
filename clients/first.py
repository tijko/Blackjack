#!/usr/bin/env python

import simplejson
import random
import itertools
import os

import pygame

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall


class Shuffle(object):

    def __init__(self):
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,
                      'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck)
        return


class Take(Shuffle):

    def card(self):
        self.card = self.deck[0]
        self.deck.pop(0) 
        return self.card


class Total(Shuffle):

    def tally(self,score):
        self.amount = 0
        for i in score:
            if self.cards.has_key(i):
                self.amount += self.cards[i] 
        if self.amount > 21 and 'ace' in score:
            for i in range(score.count('ace')):
                if self.amount > 21:
                    self.amount -= 10
        return self.amount


class Hold(Total):

    def dealer_hit(self,score):
        comp = self.tally(score)
        if comp > 16:
            return    
        if comp < 17:
            self.card = self.deck[0]
            self.deck.pop(0)
            return self.card


class Client(object):

    def __init__(self):
        pygame.init()
        self.card2_spot = 350
        self.card3_spot = 110
        self.turn = 0
        self.spot_x = 640
        self.dspot_x = 260
        self.bj_count = 0
        self.player_bj = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(1)
        self.bust = pygame.image.load(os.environ['HOME'] + 
                                      '/Pictures/images/bust.png').convert_alpha()
        self.dealer_blackjack = pygame.image.load(os.environ['HOME'] + 
                                                  '/Pictures/images/dealer_blackjack.png').convert_alpha()
        self.player_blackjack = pygame.image.load(os.environ['HOME'] + 
                                                  '/Pictures/images/player_blackjack.png').convert_alpha()
        self.dealer_wins = pygame.image.load(os.environ['HOME'] + 
                                             '/Pictures/images/dealer_wins.png').convert_alpha()
        self.player_wins = pygame.image.load(os.environ['HOME'] + 
                                             '/Pictures/images/player_wins.png').convert_alpha()
        self.tie = pygame.image.load(os.environ['HOME'] + 
                                     '/Pictures/images/tie.png').convert_alpha()
        self.stand_image = pygame.image.load(os.environ['HOME'] + 
                                             '/Pictures/images/stand.png').convert_alpha()
        self.hit_image = pygame.image.load(os.environ['HOME'] + 
                                           '/Pictures/images/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        backdrop = pygame.image.load(os.environ['HOME'] + 
                                     '/Pictures/images/black.jpg').convert()
        self.screen.blit(backdrop,(0,0))
        table = pygame.image.load(os.environ['HOME'] + 
                                  '/Pictures/images/new.png').convert_alpha()
        self.screen.blit(table,(0,50))
        banner = pygame.image.load(os.environ['HOME'] + 
                                   '/Pictures/images/banner.png').convert_alpha()
        self.screen.blit(banner,(205,505))
        decoration = pygame.image.load(os.environ['HOME'] + 
                                       '/Pictures/images/start.png').convert()
        self.screen.blit(decoration,(565,150))
        self.stand_image = pygame.image.load(os.environ['HOME'] + 
                                             '/Pictures/images/stand.png').convert_alpha()
        self.deal_image = pygame.image.load(os.environ['HOME'] + 
                                            '/Pictures/images/deal.png').convert_alpha()
        self.hit_image = pygame.image.load(os.environ['HOME'] + 
                                           '/Pictures/cards/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        pygame.display.flip()
        reactor.callLater(0.1, self.tick)

    def new_line(self, line):
        self.line = line
        spot_x = 50
        spot_y = 240
        seat = 0
        if 'deal' in self.line:
            self.__init__()
        if 'turn1' in self.line:
            self.turn += 1
            if self.player_amount == 21:
                self.turn = 0 
        if 'player' in self.line:
            pass
        if 'edge' in self.line:
            self.line = simplejson.loads(self.line)
            for i in self.line:
                if 'png' not in i:
                    edge = pygame.image.load(os.environ['HOME'] + 
                                             '/Pictures/images/edge.png').convert()
                    self.screen.blit(edge,(332,100))
                if 'png' in i:
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + i)
                    self.screen.blit(out,(self.dspot_x,100))
                    self.dspot_x += 30
        if 'dh' in self.line:
            self.line = simplejson.loads(self.line)
            for i in self.line:
                if 'png' in i:
                    self.bj_count += 1
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + i)
                    self.screen.blit(out,(self.dspot_x,100))
                    self.dspot_x += 30
        if ('png' in self.line and 
            'edge' not in self.line and 
            'card1' not in self.line and 
            'card2' not in self.line and 
            'card3' not in self.line and 
            'dh' not in self.line):
            self.line = simplejson.loads(self.line)
            for i in self.line:
                for v in i:
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + v).convert()
                    self.screen.blit(out,(spot_x,spot_y))
                    spot_x += 30
                if seat < 1:
                    spot_x += 180
                    spot_y += 120
                if seat == 1:
                    spot_x += 230
                    spot_y -= 80
                seat += 1
        if 'first' in self.line:
            self.line = simplejson.loads(self.line)
            self.score = self.line
            self.player_amount = Total().tally(self.line)
            if self.player_amount == 21:
                self.player_bj += 1
                self.turn = 0
                turn = 'turn2'
                turn = simplejson.dumps(turn)
                self.sendLine(turn)
        if 'card2' in self.line:
            self.line = simplejson.loads(self.line)
            for i in self.line:
                if 'png' in i:
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + i).convert()
                    self.screen.blit(out,(self.card2_spot,360))
                    self.card2_spot += 30
        if 'card3' in self.line:
            self.line = simplejson.loads(self.line)
            for i in self.line:
                if 'png' in i:
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + i).convert()
                    self.screen.blit(out,(self.card3_spot,240))
                    self.card3_spot += 30
        if 'score' in self.line and self.player_amount < 22:
            self.line = simplejson.loads(self.line)
            for i in self.line:
                if isinstance(i,int):
                    if self.player_amount == i and self.bj_count != 1 and self.player_bj != 1:
                        self.screen.blit(self.tie,(250,200))
                    if self.player_bj != 1 and self.bj_count == 1 and i == 21:
                        self.screen.blit(self.dealer_blackjack,(230,200))
                    if self.player_bj == 1 and self.bj_count == 1 and i < 21:
                        self.screen.blit(self.player_blackjack,(230,200))
                    if self.player_bj == 1 and self.bj_count != 1:
                        self.screen.blit(self.player_blackjack,(230,200))
                    if self.player_bj == 1 and self.bj_count == 1 and i == 21:
                        self.screen.blit(self.tie,(250,200))
                    if self.player_amount < i and i < 22 and self.bj_count != 1:
                        self.screen.blit(self.dealer_wins,(260,200))
                    if self.bj_count == 1 and i < 21 and i > self.player_amount:
                        self.screen.blit(self.dealer_wins,(260,200))
                    if self.bj_count == 1 and i < 21 and self.player_amount == i:
                        self.screen.blit(self.tie,(250,200))
                    if i > 21 and self.player_bj == 1:
                        self.screen.blit(self.player_blackjack,(230,200))
                    if i > 21 and self.player_bj != 1:
                        self.screen.blit(self.player_wins,(250,200))
                    if self.player_amount > i and self.player_bj != 1 and self.player_bj != 1:
                        self.screen.blit(self.player_wins,(250,200))
        pygame.display.flip()

    def sendLine(self, line):
        pass

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.stand_rect.collidepoint(pos) and self.turn == 1:
                    turn = 'turn2'
                    turn = simplejson.dumps(turn)
                    self.sendLine(turn)
                    self.turn = 0
                if self.hit_rect.collidepoint(pos) and self.turn == 1:
                    new_card = Take().card()
                    self.score.append(new_card[1])
                    draw =  new_card[0] + new_card[1] + '.png' 
                    out = pygame.image.load((os.environ['HOME'] + 
                                             '/Pictures/images/') + draw).convert()
                    self.screen.blit(out,(self.spot_x,280))
                    self.player_amount = Total().tally(self.score)
                    self.spot_x += 30
                    card = ['card1',draw]
                    card = simplejson.dumps(card)
                    self.sendLine(card)
                    if self.player_amount == 21:
                        self.turn = 0
                        turn = 'turn2'
                        turn = simplejson.dumps(turn)
                        self.sendLine(turn)
                    if self.player_amount > 21:
                        self.screen.blit(self.bust,(200,200))
                        self.turn = 0
                        turn = 'turn2'
                        turn = simplejson.dumps(turn)
                        self.sendLine(turn)
                    pygame.display.flip()


class BlackClientProtocol(LineReceiver):

    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self, line):
        self.recv(line)
        print line    
  

class BlackClient(ClientFactory):

    def __init__(self, client):
        self.client = client

    def buildProtocol(self, addr):
        proto = BlackClientProtocol(self.client.new_line)
        self.client.sendLine = proto.sendLine
        return proto


if __name__ == '__main__':
    c = Client()
    lc = LoopingCall(c.tick)
    lc.start(0.1)
    reactor.connectTCP('192.168.1.2', 6000, BlackClient(c))
    reactor.run()

