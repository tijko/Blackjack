import random
import pygame
import itertools
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.task import Cooperator 
from twisted.protocols.basic import LineReceiver

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(1)

bust = pygame.image.load('Pictures/cards/bust.png').convert_alpha()
dealer_blackjack = pygame.image.load('Pictures/cards/dealer_blackjack.png').convert_alpha()
player_blackjack = pygame.image.load('Pictures/cards/player_blackjack.png').convert_alpha()
dealer_wins = pygame.image.load('Pictures/cards/dealer_wins.png').convert_alpha()
player_wins = pygame.image.load('Pictures/cards/player_wins.png').convert_alpha()
tie = pygame.image.load('Pictures/cards/tie.png').convert_alpha()
stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
deal_image = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
stand_rect = screen.blit(stand_image,(630,420))
deal_rect = screen.blit(deal_image,(690,380))
hit_rect = screen.blit(hit_image,(562,445))

def default_screen():
    backdrop = pygame.image.load('Pictures/cards/black.jpg').convert()
    screen.blit(backdrop,(0,0))
    table = pygame.image.load('Pictures/cards/new.png').convert_alpha()
    screen.blit(table,(0,50))
    banner = pygame.image.load('Pictures/cards/banner.png').convert_alpha()
    screen.blit(banner,(205,505))
    decoration = pygame.image.load('Pictures/cards/start.png').convert()
    screen.blit(decoration,(565,150))
    stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
    deal_image = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
    hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
    stand_rect = screen.blit(stand_image,(630,420))
    deal_rect = screen.blit(deal_image,(690,380))
    hit_rect = screen.blit(hit_image,(562,445))
    pygame.display.flip()

## the server should send 'cards'(the hand being dealt) ##
## as clients connect give 'users' a name ##
## then i will have to put in all the logic for each user ##
## depending on whether 'user_1' or 'user_2' and so forth this will determine where to blit cards ##
## don't send the win/lose results those are all blitted locally // so send card info then blit as usual ##
## change the client scripts running on jennes/ma's machines not to be able to deal ##

## here is self.output:  card = self.output[0] + self.output[1] + 'png' ##
##  
class ChatClientProtocol(LineReceiver):
    def lineReceived(self,line):
        print (line)

class ChatClient(ClientFactory):
    def __init__(self):
        self.protocol = ChatClientProtocol

class Shuffle(object):
    def __init__(self):
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck)
        return

class Deal(Shuffle):
    def __init__(self):
        Shuffle.__init__(self)
        self.player = self.deck.pop(0) + self.deck.pop(1)
        self.dealer = self.deck.pop(0) + self.deck.pop(1)	    
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
        

def main():
    flag = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
## with the events pass the control of buttons with flags ##
## so... player_1 will be if collidepoint and flag == 1 ##
## and so on ##
                pos = pygame.mouse.get_pos()
                if stand_rect.collidepoint(pos) and flag < 1:
                ## same idea as below sending player_turn_flag to other players after turns then ending at dealer ## 
                    draw = dealer_cards[2] + dealer_cards[3] + '.png'
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    screen.blit(out,(dspot_x,100))
                    pygame.display.flip()
                    dspot_x += 30
                    if dealer_amount == 21:
                        screen.blit(dealer_blackjack,(230,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount < player_amount and flag < 1:
                        screen.blit(player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount > player_amount and flag < 1:
                        screen.blit(dealer_wins,(260,200))
                        pygame.display.flip()
                        flag += 1
                    if dealer_amount > 16 and dealer_amount == player_amount and flag < 1:
                        screen.blit(tie,(250,200))
                        pygame.display.flip()
                        flag += 1
                    while dealer_amount < 17:                    
                        new = Hold().dealer_hit(dealer_score)
                        draw = new[0] + new[1] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        screen.blit(out,(dspot_x,100))
                        dspot_x += 30
                        pygame.display.flip()
                        dealer_score.append(new[1])
                        dealer_amount = Total().tally(dealer_score)
                    if dealer_amount > 21 and flag < 1:
                        screen.blit(player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1      
                    if player_amount > dealer_amount and player_amount < 22 and flag < 1:
                        screen.blit(player_wins,(250,200))
                        pygame.display.flip()
                        flag += 1
                    if player_amount < dealer_amount and dealer_amount < 22 and flag < 1:
                        screen.blit(dealer_wins,(260,200))
                        pygame.display.flip()
                        flag += 1
                    elif dealer_amount == player_amount and flag < 1:
                        screen.blit(tie,(250,200))
                        pygame.display.flip()
                        flag += 1        
                if deal_rect.collidepoint(pos):
                    ## find out how to send each player their hand when I 'click' deal ##
                    ## and maybe some intial state // i.e. player_turn_flag that is changed depending on what I do with 'MY' turn -- and so on ##
                    flag = 0
                    default_screen()
                    deal = Deal()
                    dealer_cards = deal.dealer
                    player_hand = []
                    player_hand.append(deal.player[0]+deal.player[1]+'.png')
                    player_hand.append(deal.player[2]+deal.player[3]+'.png') 
                    spot_x = 50
                    for i in player_hand:
                        out = pygame.image.load(('Pictures/cards/') + i).convert()
                        screen.blit(out,(spot_x,240))
                        spot_x += 30
                    edge = pygame.image.load('Pictures/cards/edge.png').convert()
                    screen.blit(edge,(332,100))
                    dealer_hand = []
                    dealer_hand.append(deal.dealer[0]+deal.dealer[1]+'.png')
                    dspot_x = 260
                    for i in dealer_hand:
                        out = pygame.image.load(('Pictures/cards/') + i).convert()
                        screen.blit(out,(dspot_x,100))
                        dspot_x += 30
                    pygame.display.flip()
                    player_score = [deal.player[1], deal.player[3]]
                    dealer_score = [deal.dealer[1], deal.dealer[3]]
                    player_amount = Total().tally(player_score)
                    dealer_amount = Total().tally(dealer_score)
                    if player_amount == 21 and dealer_amount != 21:
                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        screen.blit(out,(dspot_x,100))
                        dspot_x += 30
                        screen.blit(player_blackjack,(230,200))
                        pygame.display.flip()
                        flag += 1
                    if player_amount == 21 and dealer_amount == 21:
                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        screen.blit(out,(dspot_x,100))
                        dspot_x += 30 
                        screen.blit(tie,(230,200))
                        pygame.display.flip()
                        flag += 1
                if hit_rect.collidepoint(pos) and player_amount < 21 and flag < 1:
                ## take a card and also send that info to blit on others screen ##
                ## only have to total locally because only competeting against dealer ##
                    new_card = Take().card()
                    player_score.append(new_card[1])
                    draw =  new_card[0] + new_card[1] + '.png' 
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    screen.blit(out,(spot_x,240))
                    player_amount = Total().tally(player_score)
                    spot_x += 30
                    if player_amount > 21:
                        screen.blit(bust,(200,200))
                        flag += 1
                    pygame.display.flip()
        yield

default_screen()
Cooperator().coiterate(main())
reactor.connectTCP('192.168.1.2', 6000, ChatClient())
reactor.run()


