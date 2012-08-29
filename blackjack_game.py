import random
import pygame
import itertools

class Blackjack:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(1)
        self.player_total = 0
        self.dealer_total = 0
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck) 
        self.player = self.deck.pop(0) + self.deck.pop(1)
        self.dealer = self.deck.pop(0) + self.deck.pop(0)
        player_hand = []
        player_hand.append(self.player[0]+self.player[1]+'.png')
        player_hand.append(self.player[2]+self.player[3]+'.png')
        self.bust = pygame.image.load('Pictures/cards/bust.png').convert_alpha()
        self.dealer_blackjack = pygame.image.load('Pictures/cards/dealer_blackjack.png').convert_alpha()
        self.player_blackjack = pygame.image.load('Pictures/cards/player_blackjack.png').convert_alpha()
        self.dealer_wins = pygame.image.load('Pictures/cards/dealer_wins.png').convert_alpha()
        self.player_wins = pygame.image.load('Pictures/cards/player_wins.png').convert_alpha()
        self.tie = pygame.image.load('Pictures/cards/tie.png').convert_alpha()
        backdrop = pygame.image.load('Pictures/cards/black.jpg').convert()
        self.screen.blit(backdrop,(0,0))
        table = pygame.image.load('Pictures/cards/new.png').convert_alpha()
        self.screen.blit(table,(0,0))
        banner = pygame.image.load('Pictures/cards/banner.png').convert_alpha()
        self.screen.blit(banner,(205,450))
        decoration = pygame.image.load('Pictures/cards/start.png').convert()
        self.screen.blit(decoration,(565,80))
        stand = pygame.image.load('Pictures/cards/stand.png').convert_alpha()
        self._stand = self.screen.blit(stand,(545,310))
        deal = pygame.image.load('Pictures/cards/deal.png').convert_alpha()
        self._deal = self.screen.blit(deal,(615,290))
        hit = pygame.image.load('Pictures/cards/hit.png').convert_alpha()
        self._hit = self.screen.blit(hit,(475,330))
        self.dspot_x = 260
        edge = pygame.image.load('Pictures/cards/edge.png').convert()
        self.screen.blit(edge,(332,50))
        self.flag = 0
        dealer_hand = []
        dealer_hand.append(self.dealer[0]+self.dealer[1]+'.png')
        for i in dealer_hand:
            out = pygame.image.load(('Pictures/cards/') + i).convert()
            self.screen.blit(out,(self.dspot_x,50))
            self.dspot_x += 30
        self.spot_x = 140
        for i in player_hand:
            out = pygame.image.load(('Pictures/cards/') + i).convert()
            self.screen.blit(out,(self.spot_x,265))
            self.spot_x += 30
            pygame.display.flip()

    def score(self):
        self.player_total = 0
        self.dealer_total = 0
        for i in self.player:
            if self.cards.has_key(i):
                self.player_total += self.cards[i] 
        for i in self.dealer:
            if self.cards.has_key(i):
                self.dealer_total += self.cards[i]
        if self.dealer_total > 21 and 'ace' in self.dealer:
            deduct = self.dealer.count('ace') * 10
            self.dealer_total -= deduct 
        if self.player_total > 21 and 'ace' in self.player:
            deduct = self.player.count('ace') * 10
            self.player_total -= deduct

    def deal(self):
        self.flag = 0
        self.__init__()
        self.score()
        if self.player_total == 21 and self.dealer_total != 21:
            next = self.dealer[2] + self.dealer[3] + '.png'
            out = pygame.image.load(('Pictures/cards/') + next).convert()
            self.screen.blit(out,(self.dspot_x,50))
            pygame.display.flip()
            self.dspot_x += 30
            self.screen.blit(self.player_blackjack,(230,200))
            pygame.display.flip()
            self.flag += 1
            self.main()
            return
        if self.player_total == 21 and self.dealer_total == 21:
            next = self.dealer[2] + self.dealer[3] + '.png'
            out = pygame.image.load(('Pictures/cards/') + next).convert()
            self.screen.blit(out,(self.dspot_x,50))
            pygame.display.flip()
            self.dspot_x += 30 
            self.screen.blit(self.tie,(230,200))
            pygame.display.flip()
            self.flag += 1
            self.main()
            return

    def hit(self):
        self.player += self.deck[0] 
        next = self.deck[0][0] + self.deck[0][1] + '.png' 
        out = pygame.image.load(('Pictures/cards/') + next).convert()
        self.screen.blit(out,(self.spot_x,265))
        pygame.display.flip()
        self.deck.pop(0)
        self.score()
        self.spot_x += 30
        if self.player_total > 21:
            self.screen.blit(self.bust,(200,200))
            pygame.display.flip()
            self.flag += 1
            self.main()            

    def stand(self):
        self.flag += 1
        next = self.dealer[2] + self.dealer[3] + '.png'
        out = pygame.image.load(('Pictures/cards/') + next).convert()
        self.screen.blit(out,(self.dspot_x,50))
        pygame.display.flip()
        self.dspot_x += 30
        if self.dealer_total == 21:
            self.screen.blit(self.dealer_blackjack,(250,200))
            pygame.display.flip()
            self.main()
            return
        if self.dealer_total > 16:
            if self.dealer_total > self.player_total:
                self.screen.blit(self.dealer_wins,(240,200))
                pygame.display.flip()
            if self.player_total > self.dealer_total:
                self.screen.blit(self.player_wins,(240,200))
                pygame.display.flip()
            if self.player_total == self.dealer_total:
                self.screen.blit(self.tie,(240,200))
                pygame.display.flip()
            self.main()
            return
        while self.dealer_total < 17 and self.dealer_total < self.player_total:
            self.dealer += self.deck[0]
            next = self.deck[0][0] + self.deck[0][1] + '.png'
            out = pygame.image.load(('Pictures/cards/') + next).convert()
            self.screen.blit(out,(self.dspot_x,50))
            pygame.display.flip()
            self.deck.pop(0)
            self.dspot_x += 30
            self.score()
            if self.dealer_total > 21:
                self.screen.blit(self.player_wins,(250,200))
                pygame.display.flip()
                self.main()
                return
        if self.player_total > self.dealer_total:
            self.screen.blit(self.player_wins,(260,200))
            pygame.display.flip()
        if self.dealer_total > self.player_total:
            self.screen.blit(self.dealer_wins,(260,200))
            pygame.display.flip()
        elif self.dealer_total == self.player_total:
            self.screen.blit(self.tie,(250,200))
            pygame.display.flip()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self._stand.collidepoint(pos) and self.flag == 0:
                        self.stand()
                    if self._deal.collidepoint(pos):
                        self.deal()
                    if self._hit.collidepoint(pos) and self.player_total < 22 and self.flag == 0: 
                        self.hit()
             
Blackjack().main()

