import random
import pygame
import itertools
from twisted.protocols import basic
from twisted.internet import reactor, protocol


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
stand_rect = screen.blit(stand_image,(545,310))
deal_rect = screen.blit(deal_image,(615,290))
hit_rect = screen.blit(hit_image,(475,330))

def default_screen():
    backdrop = pygame.image.load('Pictures/cards/black.jpg').convert()
    screen.blit(backdrop,(0,0))
    table = pygame.image.load('Pictures/cards/new.png').convert_alpha()
    screen.blit(table,(0,0))
    banner = pygame.image.load('Pictures/cards/banner.png').convert_alpha()
    screen.blit(banner,(205,450))
    decoration = pygame.image.load('Pictures/cards/start.png').convert()
    screen.blit(decoration,(565,80))
    stand_image = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
    deal_image = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
    hit_image = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
    stand_rect = screen.blit(stand_image,(545,310))
    deal_rect = screen.blit(deal_image,(615,290))
    hit_rect = screen.blit(hit_image,(475,330))
    pygame.display.flip()

class Players(object):
    def __init__(self):
        self.player_list = []
        return

#	while ***'something to wait for me to signal, that all players have joined'***:
#		'have server wait for clients to come in'
#		player_list.append('client')
#	def __init__(self):
#		self.player_names = []
#		count = 0
#		for player in player_list:
#			name = 'player' + '_' + str(count)
#    	    count += 1
#		self.player_name.append(name)
	
## create connection for each interaction ##
## i.e. mousedown buttons :: but have to 'wait' for turn ##
## not sure if I should run a separate script for "listening server" ##
## probably ##
## create this into separate 'main' function 'looping' ##

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
#        players = Players()
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
#    Players()  
    flag = 0
    default_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if stand_rect.collidepoint(pos) and flag < 1: 
                    draw = dealer_cards[2] + dealer_cards[3] + '.png'
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    screen.blit(out,(dspot_x,50))
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
                        screen.blit(out,(dspot_x,50))
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
                    flag = 0
                    default_screen()
                    deal = Deal()
                    dealer_cards = deal.dealer
                ## this will be a list of of players with new version ##
                    player_hand = []
                    player_hand.append(deal.player[0]+deal.player[1]+'.png')
                    player_hand.append(deal.player[2]+deal.player[3]+'.png') 
                    spot_x = 140
                    for i in player_hand:
                        out = pygame.image.load(('Pictures/cards/') + i).convert()
                        screen.blit(out,(spot_x,265))
                        spot_x += 30
                    edge = pygame.image.load('Pictures/cards/edge.png').convert()
                    screen.blit(edge,(332,50))
                    dealer_hand = []
                    dealer_hand.append(deal.dealer[0]+deal.dealer[1]+'.png')
                    dspot_x = 260
                    for i in dealer_hand:
                        out = pygame.image.load(('Pictures/cards/') + i).convert()
                        screen.blit(out,(dspot_x,50))
                        dspot_x += 30
                    pygame.display.flip()
                    player_score = [deal.player[1], deal.player[3]]
                    dealer_score = [deal.dealer[1], deal.dealer[3]]
                    player_amount = Total().tally(player_score)
                    dealer_amount = Total().tally(dealer_score)
                    if player_amount == 21 and dealer_amount != 21:
                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        screen.blit(out,(dspot_x,50))
                        dspot_x += 30
                        screen.blit(player_blackjack,(230,200))
                        pygame.display.flip()
                        flag += 1
                    if player_amount == 21 and dealer_amount == 21:
                        draw = deal.dealer[2] + deal.dealer[3] + '.png'
                        out = pygame.image.load(('Pictures/cards/') + draw).convert()
                        screen.blit(out,(dspot_x,50))
                        dspot_x += 30 
                        screen.blit(tie,(230,200))
                        pygame.display.flip()
                        flag += 1
                if hit_rect.collidepoint(pos) and player_amount < 21 and flag < 1:
                    new_card = Take().card()
                    player_score.append(new_card[1])
                    draw =  new_card[0] + new_card[1] + '.png' 
                    out = pygame.image.load(('Pictures/cards/') + draw).convert()
                    screen.blit(out,(spot_x,265))
                    player_amount = Total().tally(player_score)
                    spot_x += 30
                    if player_amount > 21:
                        screen.blit(bust,(200,200))
                        flag += 1
                    pygame.display.flip()
 

if __name__ == "__main__":
    main()

