import random
import itertools
import simplejson

import pygame

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall


class Shuffle(object):
    """
    Class for setting up the deck and 
    accessing cards.
    """
    def __init__(self):
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,
                      'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck)
        return


class Deal(Shuffle):
    """
    Class that handles passing cards to dealer or
    player when called.
    """ 
    def __init__(self):
        Shuffle.__init__(self)
        self.player = self.deck.pop(0) + self.deck.pop(1)
        self.dealer = self.deck.pop(0) + self.deck.pop(1)       


class Take(Shuffle):
    """
    Class for 'hit'ing a player/dealer
    when asked for.
    """
    def card(self):
        self.card = self.deck[0]
        self.deck.pop(0) 
        return self.card


class Total(Shuffle):
    """
    Class that will score a hand.
    """
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
    """
    Class to call when all players
    are done taking cards.
    """
    def dealer_hit(self,score):
        comp = self.tally(score)
        if comp > 16:
            return    
        if comp < 17:
            self.card = self.deck[0]
            self.deck.pop(0)
            return self.card


class Client(object):
    """
    Class to handle setting default screen,
    to check data received from the server,
    send data to the server, and handle
    pygame events.
    """
    def __init__(self):
        pygame.init()
        self.card1_spot = 640
        self.card2_spot = 350
        self.turn = 0
        self.bj = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(1)
        self.bust = pygame.image.load('Pictures/cards/bust.png').convert_alpha()
        self.dealer_blackjack = pygame.image.load('Pictures/cards/dealer_blackjack.png').convert_alpha()
        self.player_blackjack = pygame.image.load('Pictures/cards/player_blackjack.png').convert_alpha()
        self.dealer_wins = pygame.image.load('Pictures/cards/dealer_wins.png').convert_alpha()
        self.player_wins = pygame.image.load('Pictures/cards/player_wins.png').convert_alpha()
        self.tie = pygame.image.load('Pictures/cards/tie.png').convert_alpha()
        self.stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
        self.deal_image = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
        self.hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.deal_rect = self.screen.blit(self.deal_image,(690,380))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        backdrop = pygame.image.load('Pictures/cards/black.jpg').convert()
        self.screen.blit(backdrop,(0,0))
        table = pygame.image.load('Pictures/cards/new.png').convert_alpha()
        self.screen.blit(table,(0,50))
        banner = pygame.image.load('Pictures/cards/banner.png').convert_alpha()
        self.screen.blit(banner,(205,505))
        decoration = pygame.image.load('Pictures/cards/start.png').convert()
        self.screen.blit(decoration,(565,150))
        self.stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
        self.deal_image = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
        self.hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
        self.deal_rect = self.screen.blit(self.deal_image,(690,380))
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        pygame.display.flip()
        reactor.callLater(0.1, self.tick)

    def new_line(self, line):
        self.line = line
        self.line = simplejson.loads(self.line)
        if 'card1' in self.line:
            for i in self.line:
                if 'png' in i:
                    out = pygame.image.load(('Pictures/cards/') + i).convert()
                    self.screen.blit(out,(self.card1_spot,280))
                    self.card1_spot += 30
                    pygame.display.flip()
        if 'card2' in self.line:
            for i in self.line:
                if 'png' in i:
                    out = pygame.image.load(('Pictures/cards/') + i).convert()
                    self.screen.blit(out,(self.card2_spot,360))
                    self.card2_spot += 30
                    pygame.display.flip()
        if 'turn3' in self.line:
            self.turn = 1
            if self.player_amount == 21 and self.dealer_amount != 21 and self.turn == 1:
                draw = self.deal.dealer[2] + self.deal.dealer[3] + '.png'
                out = pygame.image.load(('Pictures/cards/') + draw).convert()
                self.screen.blit(out,(self.dspot_x,100))
                self.dspot_x += 30
                self.screen.blit(self.player_blackjack,(230,200))
                self.turn = 0
                draw = self.deal.dealer[2] + self.deal.dealer[3] + '.png'
                out = pygame.image.load(('Pictures/cards/') + draw).convert()
                self.screen.blit(out,(self.dspot_x,100))
                self.dspot_x += 30
                dh = ['dh', draw]
                dh = simplejson.dumps(dh)
                self.sendLine(dh)
                while self.dealer_amount < 17:                    
                    new = Hold().dealer_hit(self.dealer_score)
                    draw = new[0] + new[1] + '.png'
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    self.screen.blit(out,(self.dspot_x,100))
                    self.dspot_x += 30
                    dh = ['dh', draw]
                    dh = simplejson.dumps(dh)
                    self.sendLine(dh)
                    self.dealer_score.append(new[1])
                    self.dealer_amount = Total().tally(self.dealer_score)
                score = ['score',self.dealer_amount]
                score = simplejson.dumps(score)
                self.sendLine(score)
            if self.player_amount == 21 and self.dealer_amount == 21 and self.turn == 1:
                draw = self.deal.dealer[2] + self.deal.dealer[3] + '.png'
                out = pygame.image.load(('Pictures/cards/') + draw).convert()
                self.screen.blit(out,(self.dspot_x,100))
                self.dspot_x += 30 
                self.screen.blit(self.tie,(230,200))
                self.turn = 0
                score = ['score',self.dealer_amount]
                score = simplejson.dumps(score)
                self.sendLine(score)
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
                    self.turn = 0
                    draw = self.deal.dealer[2] + self.deal.dealer[3] + '.png'
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    self.screen.blit(out,(self.dspot_x,100))
                    self.dspot_x += 30
                    dh = ['dh', draw]
                    dh = simplejson.dumps(dh)
                    self.sendLine(dh)
                    if self.dealer_amount == 21:
                        self.screen.blit(self.dealer_blackjack,(230,200))
                        self.bj += 1
                    if self.dealer_amount > 16 and self.dealer_amount < self.player_amount:
                        self.screen.blit(self.player_wins,(250,200))
                    if self.dealer_amount > 16 and self.dealer_amount > self.player_amount and self.dealer_amount != 21:
                        self.screen.blit(self.dealer_wins,(260,200))
                    if self.dealer_amount > 16 and self.dealer_amount == self.player_amount and self.bj != 1:
                        self.screen.blit(self.tie,(250,200))
                    while self.dealer_amount < 17:                    
                        new = Hold().dealer_hit(self.dealer_score)
                        draw = new[0] + new[1] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        self.screen.blit(out,(self.dspot_x,100))
                        self.dspot_x += 30
                        dh = ['dh', draw]
                        dh = simplejson.dumps(dh)
                        self.sendLine(dh)
                        self.dealer_score.append(new[1])
                        self.dealer_amount = Total().tally(self.dealer_score)
                        if self.dealer_amount > 21:
                            self.screen.blit(self.player_wins,(250,200))
                        if self.player_amount > self.dealer_amount and self.player_amount < 22 and self.dealer_amount > 16:
                            self.screen.blit(self.player_wins,(250,200))
                        if self.player_amount < self.dealer_amount and self.dealer_amount < 22 and self.dealer_amount > 16:
                            self.screen.blit(self.dealer_wins,(260,200))
                        elif self.dealer_amount == self.player_amount and self.dealer_amount > 16:
                            self.screen.blit(self.tie,(250,200))
                    score = ['score',self.dealer_amount]
                    score = simplejson.dumps(score)
                    self.sendLine(score)
                    pygame.display.flip()
                if self.deal_rect.collidepoint(pos):
                    allhands = []
                    self.__init__()
                    new = 'deal'
                    new = simplejson.dumps(new)
                    self.sendLine(new)
                    self.deal = Deal()
                    self.spot_x = 50
                    spot_y = 240
                    suit = 0
                    card = 1
                    seat = 0
                ## could work this differently ##
                    for player in range(3):
                        player_hand = []
                        self.deal.__init__()
                        fresh_hand = self.deal.player
                        player_hand.append(fresh_hand[suit] + fresh_hand[card] + '.png')
                        player_hand.append(fresh_hand[suit + 2] + fresh_hand[card + 2] + '.png') 
                        for i in player_hand:
                            out = pygame.image.load(('Pictures/cards/') + i).convert()
                            self.screen.blit(out,(self.spot_x,spot_y))
                            self.spot_x += 30
                        if seat == 0:
                            self.player_score = [fresh_hand[1], fresh_hand[3]]
                        if seat < 1:
                            self.spot_x += 180
                            spot_y += 120
                        if seat == 1:
                            self.spot_x += 230
                            spot_y -= 80
                            second = [i for i in fresh_hand]
                            second.append('second')
                            second = simplejson.dumps(second)
                            self.sendLine(second)
                        if seat == 2:
                            first = [i for i in fresh_hand]
                            first.append('first')
                            first = simplejson.dumps(first)
                            self.sendLine(first)
                        seat += 1
                        allhands.append(player_hand)
                    allhands = simplejson.dumps(allhands)
                    self.sendLine(allhands)
                    edge = pygame.image.load('Pictures/cards/edge.png').convert()
                    self.screen.blit(edge,(332,100))
                    dealer_hand = []
                    dealer_hand.append(self.deal.dealer[0] + self.deal.dealer[1] + '.png')
                    self.dspot_x = 260
                    for i in dealer_hand:
                        out = pygame.image.load(('Pictures/cards/') + i).convert()
                        self.screen.blit(out,(self.dspot_x,100))
                        self.dspot_x += 30
                    pygame.display.flip()
                    self.dealer_score = [self.deal.dealer[1], self.deal.dealer[3]]
                    self.player_amount = Total().tally(self.player_score)
                    self.dealer_amount = Total().tally(self.dealer_score)
                    self.spot_x = 110
                    dealer_send = dealer_hand.append('edge')
                    dealer_send = simplejson.dumps(dealer_hand)
                    self.sendLine(dealer_send)
                    turn = 'turn1'
                    turn = simplejson.dumps(turn)
                    self.sendLine(turn)
                if self.hit_rect.collidepoint(pos) and self.player_amount < 21 and self.turn == 1:
                    new_card = Take().card()
                    self.player_score.append(new_card[1])
                    draw =  new_card[0] + new_card[1] + '.png' 
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    self.screen.blit(out,(self.spot_x,240))
                    self.player_amount = Total().tally(self.player_score)
                    self.spot_x += 30
                    card = ['card3', draw]
                    card = simplejson.dumps(card)
                    self.sendLine(card)
                    if self.player_amount > 21:
                        self.screen.blit(self.bust,(200,200))
                        self.turn = 0
                        draw = self.deal.dealer[2] + self.deal.dealer[3] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        self.screen.blit(out,(self.dspot_x,100))
                        self.dspot_x += 30
                        dh = ['dh', draw]
                        dh = simplejson.dumps(dh)
                        self.sendLine(dh)
                        while self.dealer_amount < 17:                    
                            new = Hold().dealer_hit(self.dealer_score)
                            draw = new[0] + new[1] + '.png'
                            out = pygame.image.load(('Pictures/cards/') + draw).convert()
                            self.screen.blit(out,(self.dspot_x,100))
                            self.dspot_x += 30
                            dh = ['dh', draw]
                            dh = simplejson.dumps(dh)
                            self.sendLine(dh)
                            self.dealer_score.append(new[1])
                            self.dealer_amount = Total().tally(self.dealer_score)
                        score = ['score',self.dealer_amount]
                        score = simplejson.dumps(score)
                        self.sendLine(score)
                    pygame.display.flip()


class BlackClientProtocol(LineReceiver):
    """ 
    Class client for receiving data
    from the server.
    """
    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self, line):
        self.recv(line)
        print line


class BlackClient(ClientFactory):
    """
    Class that builds protocol instances
    to send to the server.
    """
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


