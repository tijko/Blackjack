import simplejson
import pygame
import random
import itertools
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall

class Shuffle(object):
    def __init__(self):
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck)
        return

class Take(Shuffle):
    def card(self):
        Shuffle.__init__(self)
        self.card = self.deck[0]
        self.deck.pop(0) 
        return self.card

class Total(Shuffle):
    def tally(self,score):
        Shuffle.__init__(self)
        self.amount = 0
        for i in score:
            if self.cards.has_key(i):
                self.amount += self.cards[i] 
        if self.amount > 21 and 'ace' in score:
            deduct = score.count('ace') * 10
            self.amount -= deduct 
        return self.amount

class Hold(Total):
    def dealer_hit(self,score):
        Total.__init__(self)
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
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(1)
        self.bust = pygame.image.load('Pictures/cards/bust.png').convert_alpha()
        self.dealer_blackjack = pygame.image.load('Pictures/cards/dealer_blackjack.png').convert_alpha()
        self.player_blackjack = pygame.image.load('Pictures/cards/player_blackjack.png').convert_alpha()
        self.dealer_wins = pygame.image.load('Pictures/cards/dealer_wins.png').convert_alpha()
        self.player_wins = pygame.image.load('Pictures/cards/player_wins.png').convert_alpha()
        self.tie = pygame.image.load('Pictures/cards/tie.png').convert_alpha()
        self.stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
        self.hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
        self.stand_rect = self.screen.blit(self.stand_image,(630,420))
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
        self.hit_rect = self.screen.blit(self.hit_image,(562,445))
        pygame.display.flip()
        reactor.callLater(0.1, self.tick)

    def new_line(self, line):
        self.line = line
        self.line = simplejson.loads(self.line)

    def tick(self):
        flag = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.stand_rect.collidepoint(pos) and flag < 1 and self.line == 'turn1':
                    draw = dealer_cards[2] + dealer_cards[3] + '.png'
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    self.screen.blit(out,(dspot_x,100))
                    pygame.display.flip()
                    dspot_x += 30
                    if dealer_amount == 21:
                        self.screen.blit(self.dealer_blackjack,(230,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount < player_amount and flag < 1:
                        self.screen.blit(self.player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount > player_amount and flag < 1:
                        self.screen.blit(self.dealer_wins,(260,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount == player_amount and flag < 1:
                        self.screen.blit(tie,(250,200))
                        pygame.display.flip()
                        flag += 1
                    while dealer_amount < 17:                    
                        new = Hold().dealer_hit(dealer_score)
                        draw = new[0] + new[1] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        self.screen.blit(out,(dspot_x,100))
                        dspot_x += 30
                        pygame.display.flip()
                        dealer_score.append(new[1])
                        dealer_amount = Total().tally(dealer_score)
                    if dealer_amount > 21 and flag < 1:
                        self.screen.blit(self.player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1      
                    if player_amount > dealer_amount and player_amount < 22 and flag < 1:
                        self.screen.blit(self.player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1
                    if player_amount < dealer_amount and dealer_amount < 22 and flag < 1:
                        self.screen.blit(self.dealer_wins,(260,200))
                        pygame.display.flip()
                        flag += 1
                    elif dealer_amount == player_amount and flag < 1:
                        self.screen.blit(self.tie,(250,200))
                        pygame.display.flip()
                        flag += 1        

#                    edge = pygame.image.load('Pictures/cards/edge.png').convert()
#                    self.screen.blit(edge,(332,100))
#                    dealer_hand = []
#                    dealer_hand.append(deal.dealer[0]+deal.dealer[1]+'.png')
#                    dspot_x = 260

#                    for i in dealer_hand:
#                        out = pygame.image.load(('Pictures/cards/') + i).convert()
#                        self.screen.blit(out,(dspot_x,100))
#                        dspot_x += 30
#                    pygame.display.flip()
#                    player_score = [deal.player[1], deal.player[3]]
#                    dealer_score = [deal.dealer[1], deal.dealer[3]]
#                    player_amount = Total().tally(player_score)
#                    dealer_amount = Total().tally(dealer_score)
#                    if player_amount == 21 and dealer_amount != 21:
#                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
#                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
#                        self.screen.blit(out,(dspot_x,100))
#                        dspot_x += 30
#                        self.screen.blit(self.player_blackjack,(230,200))
#                        pygame.display.flip()
#                        flag += 1
#                    if player_amount == 21 and dealer_amount == 21:
#                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
#                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
#                        self.screen.blit(out,(dspot_x,100))
#                        dspot_x += 30 
#                        self.screen.blit(self.tie,(230,200))
#                        pygame.display.flip()
#                        flag += 1

                if self.hit_rect.collidepoint(pos) and player_amount < 21 and flag < 1 and self.line == 'turn1':
                    new_card = Take().card()
                    player_score.append(new_card[1])
                    draw =  new_card[0] + new_card[1] + '.png' 
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    self.screen.blit(out,(spot_x,240))
                    player_amount = Total().tally(player_score)
                    spot_x += 30
                    if player_amount > 21:
                        self.screen.blit(self.bust,(200,200))
                        flag += 1
                    pygame.display.flip()

class BlackClientProtocol(LineReceiver):
    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self, line):
        client = Client()
        spot_x = 50
        spot_y = 240
        seat = 0
        self.recv(line)
        if 'turn1' in line:
            line = ''
        if 'player' in line:
            pass
        if 'png' in line:
            line = simplejson.loads(line)
            for i in line:
                for v in i:
                    out = pygame.image.load(('Pictures/cards/') + v).convert()
                    client.screen.blit(out,(spot_x,spot_y))
                    spot_x += 30
                if seat < 1:
                    spot_x += 180
                    spot_y += 120
                if seat == 1:
                    spot_x += 230
                    spot_y -= 80
                seat += 1
        print line
        pygame.display.flip()

class BlackClient(ClientFactory):
    def __init__(self, recv):
        self.recv = recv

    def buildProtocol(self, addr):
        return BlackClientProtocol(self.recv)

if __name__ == '__main__':
    c = Client()
    lc = LoopingCall(c.tick)
    lc.start(0.1)
    reactor.connectTCP('192.168.1.2', 6000, BlackClient(c.new_line))
    reactor.run()
