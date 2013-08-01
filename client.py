#!/usr/bin/env python

import simplejson
import sys
import os

import pygame

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall

from lib.actions import Shuffle, Deal, Take, Hold, Total

PATH = os.path.abspath('')


class Client(object):
    """
    Class to handle setting default screen, to check data received from the server,
    send data to the server, and handle pygame events.
    """
    def __init__(self):
        pygame.init()
        self.turn = 0
        self.deal_lock = 1
        self.pname = ''
        self.positions = [[50, 240], [230, 360], [460, 280]]
        self.dspot_x = 290
        self.dealer_bj = False
        self.player_bj = False
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(1)
        self.bust = pygame.image.load(PATH + '/images/bust.png').convert_alpha()
        self.dealer_blackjack = pygame.image.load(PATH + 
                                                  '/images/dealer_blackjack.png').convert_alpha()
        self.player_blackjack = pygame.image.load(PATH + 
                                                  '/images/player_blackjack.png').convert_alpha()
        self.dealer_wins = pygame.image.load(PATH + 
                                             '/images/dealer_wins.png').convert_alpha()
        self.player_wins = pygame.image.load(PATH + 
                                             '/images/player_wins.png').convert_alpha()
        self.tie = pygame.image.load(PATH + '/images/tie.png').convert_alpha()
        self.stand_image = pygame.image.load(PATH + 
                                             '/images/stand.png').convert_alpha()
        self.deal_image = pygame.image.load(PATH + 
                                            '/images/deal.png').convert_alpha()
        self.hit_image = pygame.image.load(PATH + 
                                           '/images/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.deal_rect = self.screen.blit(self.deal_image,(690,380))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        backdrop = pygame.image.load(PATH + 
                                     '/images/black.jpg').convert()
        self.screen.blit(backdrop,(0,0))
        table = pygame.image.load(PATH + '/images/new.png').convert_alpha()
        self.screen.blit(table,(0,50))
        banner = pygame.image.load(PATH + '/images/banner.png').convert_alpha()
        self.screen.blit(banner,(205,505))
        decoration = pygame.image.load(PATH + '/images/start.png').convert()
        self.screen.blit(decoration,(565,150))
        self.stand_image = pygame.image.load(PATH + 
                                             '/images/stand.png').convert_alpha()
        self.deal_image = pygame.image.load(PATH + 
                                            '/images/deal.png').convert_alpha()
        self.hit_image = pygame.image.load(PATH + '/images/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.deal_rect = self.screen.blit(self.deal_image,(690,380))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        pygame.display.flip()
        # twisted callLater method to switch between pygame events method and the twisted signals 
        reactor.callLater(0.1, self.tick)

    def results(self):
        if self.dealer_bj and not self.player_bj:
            self.screen.blit(self.dealer_blackjack, (230, 200))
        elif self.player_bj and not self.dealer_bj:
            self.screen.blit(self.player_blackjack, (230, 200))
        elif self.dealer_amount > self.player_amount:
            self.screen.blit(self.dealer_wins,(260, 200))
        elif self.dealer_amount == self.player_amount:
            self.screen.blit(self.tie,(250, 200))
        elif self.dealer_amount < self.player_amount:
            self.screen.blit(self.player_wins,(250, 200))
        pygame.display.flip()

    def new_line(self, line):
        self.line = line
        self.line = simplejson.loads(self.line)
        if 'Table Full' in self.line:
            reactor.stop()
            pygame.display.quit()
            print "Table Full"
            return
        if 'players_list' in self.line:
            if self.pname == '':
                self.pname = self.line[-1]
                self.pspot = int(self.pname[-1])
                score = simplejson.dumps(['allscores'] + [0 for i in self.line[1:]])
                self.sendLine(score)
            self.playrlst = self.line[1:]

        if self.line[0] == 'Deal':
            self.__init__()
            self.deal_lock = 0
            self.player_score = self.line[self.pspot][2] 
            self.player_amount = Total().tally(self.player_score)
            self.player_hand = self.line[self.pspot][:2]
            for i in self.line[1:]: # rewrite to map each player to position
                for j in i[:-1]:
                    out = pygame.image.load((PATH + '/images/') + j).convert()
                    self.screen.blit(out, (self.positions[self.line[1:].index(i)][0], 
                                           self.positions[self.line[1:].index(i)][1]))
                    self.positions[self.line[1:].index(i)][0] += 30
            pygame.display.flip() 

        if 'edge.png' in self.line:
            edge = pygame.image.load(PATH + '/images/edge.png').convert()
            self.screen.blit(edge,(332,100))
            out = pygame.image.load((PATH + '/images/') + self.line[0]).convert()
            self.screen.blit(out, (260, 100))
            self.dealer_score = self.line[1] 
            self.dealer_amount = Total().tally(self.dealer_score)
            self.dealer_hand = [self.line[0]]
            pygame.display.flip()

        if 'card' in self.line:
            if self.line[1] == self.pspot:
                out = pygame.image.load((PATH + '/images/') + self.line[2]).convert()
                self.screen.blit(out, (self.positions[self.pspot - 1][0], 
                                       self.positions[self.pspot - 1][1]))
                self.positions[self.pspot - 1][0] += 30
                self.player_score.append(self.line[3])
                self.player_amount = Total().tally(self.player_score)
                self.player_hand.append(self.line[2])
                if self.player_amount >= 21:
                    self.turn = 0
                    turn = 'turn' + str(self.pspot + 1)
                    turn = simplejson.dumps(turn)
                    self.allscores[self.pspot] = self.player_amount
                    score = simplejson.dumps(self.allscores)
                    self.sendLine(score)
                    self.sendLine(turn)
                    if self.player_amount > 21:
                        self.screen.blit(self.bust, (200, 200))
            if self.line[1] != self.pspot:
                out = pygame.image.load((PATH + '/images/') + self.line[2]).convert()
                self.screen.blit(out, (self.positions[self.line[1] - 1][0], 
                                       self.positions[self.line[1] - 1][1]))
                self.positions[self.line[1] - 1][0] += 30
            pygame.display.flip()

        if 'turn' in self.line and int(self.line[-1]) == self.pspot:
            if self.player_amount == 21:
                turn = 'turn' + str(self.pspot + 1)
                turn = simplejson.dumps(turn)
                self.player_bj = True
                self.allscores[self.pspot] = 'Blackjack'
                score = simplejson.dumps(self.allscores)
                self.sendLine(score)
                self.sendLine(turn)
            else:
                self.turn = 1

        if 'dh' in self.line:
            out = pygame.image.load((PATH + '/images/') + self.line[0]).convert()
            self.screen.blit(out,(self.dspot_x, 100))
            self.dspot_x += 30
            self.dealer_score.append(self.line[2])
            self.dealer_amount = Total().tally(self.dealer_score)
            self.dealer_hand.append(self.line[0])
            pygame.display.flip()

        if ('turn' in self.line and 
            int(self.line[-1]) > len(self.playrlst) and 
            self.pspot == 1):
            if any(i < 22 for i in self.allscores[1:]): 
                while self.dealer_amount < 17:
                    self.deal = Deal()
                    self.deal.__init__()
                    dh = [self.deal.dealer[0] + self.deal.dealer[1] + '.png',
                          'dh', self.deal.dealer[1] 
                         ]
                    dh = simplejson.dumps(dh)
                    self.sendLine(dh)
                    self.dealer_score.append(self.deal.dealer[1])
                    self.dealer_amount = Total().tally(self.dealer_score)
                    if len(self.dealer_score) == 2 and self.dealer_amount == 21:
                        self.dealer_bj = True
                dealer_score = simplejson.dumps(['dealer_score', self.dealer_amount])
                self.sendLine(dealer_score)
            else:
                self.dealer_amount = Total().tally(self.dealer_score)
                dealer_score = simplejson.dumps(['dealer_score', self.dealer_amount])
                self.sendLine(dealer_score)
                self.deal = Deal()
                self.deal.__init__()
                dh = [self.deal.dealer[0] + self.deal.dealer[1] + '.png',
                      'dh', self.deal.dealer[1]
                     ]
                dh = simplejson.dumps(dh)
                self.sendLine(dh)
            lock = simplejson.dumps('unlock')
            self.sendLine(lock)

        if 'allscores' in self.line:                          
            self.allscores = self.line

        if 'unlock' in self.line:
            self.deal_lock = 1

        if 'dealer_score' in self.line:
            self.dealer_amount = self.line[1]
            if self.player_amount < 22:
                if self.dealer_amount < 22:
                    self.results()
                else:
                    if self.player_bj:
                        self.screen.blit(self.player_blackjack, (230, 200))
                    else:
                        self.screen.blit(self.player_wins, (250, 200))
                    pygame.display.flip()
               
    def tick(self):
        # pygame events func. #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                reactor.stop()
                pygame.display.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # gets mouse coordinates if mouse clicked #
                pos = pygame.mouse.get_pos()
                # checks if 'pos' is on 'stand_rect' #
                if self.stand_rect.collidepoint(pos) and self.turn == 1:
                    self.turn = 0
                    self.allscores[self.pspot] = self.player_amount
                    score = simplejson.dumps(self.allscores)
                    self.sendLine(score)
                    turn = 'turn' + str(self.pspot + 1)
                    turn = simplejson.dumps(turn)
                    self.sendLine(turn)
                if self.deal_rect.collidepoint(pos) and self.deal_lock == 1:
                    allhands = ['Deal']
                    self.deal = Deal()
                    for player in self.playrlst:
                        self.deal.__init__()
                        player_hand = [self.deal.player[0] + self.deal.player[1] + '.png',                        
                                       self.deal.player[2] + self.deal.player[3] + '.png',
                                       [self.deal.player[1], self.deal.player[3]]
                                      ]
                        allhands.append(player_hand)
                    allhands = simplejson.dumps(allhands)
                    self.sendLine(allhands)
                    dealer_hand = [self.deal.dealer[0] + self.deal.dealer[1] + '.png',
                                   [self.deal.dealer[1]],
                                   'edge.png'
                                  ]
                    dealer_send = simplejson.dumps(dealer_hand)
                    self.sendLine(dealer_send)
                    turn = 'turn1'
                    turn = simplejson.dumps(turn)
                    self.sendLine(turn)      
                if (self.hit_rect.collidepoint(pos) and 
                    self.player_amount < 21 and 
                    self.turn == 1):
                    new_card = Take().card()    
                    card = ['card', self.pspot, 
                            new_card[0] + new_card[1] + '.png',
                            new_card[1]]
                    card = simplejson.dumps(card)
                    self.sendLine(card)


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
        proto = BlackClientProtocol(self.client.new_line)
        self.client.sendLine = proto.sendLine
        return proto


if __name__ == '__main__':
    c = Client()
    # LoopingCall method to keep checking 'tick' method for pygame events 
    lc = LoopingCall(c.tick)
    lc.start(0.1)
    reactor.connectTCP('192.168.1.5', 6000, BlackClient(c))
    reactor.run()
