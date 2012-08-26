import random
import pygame
import itertools

class Blackjack:
    def __init__(self):
        self.player_total = 0
        self.dealer_total = 0
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        random.shuffle(self.deck) 
        self.player = self.deck.pop(0) + self.deck.pop(1)
        self.dealer = self.deck.pop(0) + self.deck.pop(0)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.table = pygame.image.load('Pictures/cards/felt.jpg').convert()

    def score(self):
        self.player_total = 0
        self.dealer_total = 0
        for i in self.player:
            if self.cards.has_key(i):
                self.player_total += self.cards[i] 
        for i in self.dealer:
            if self.cards.has_key(i):
                self.dealer_total += self.cards[i]

    def show(self):
        self.score()
        print "Player has %s and total %d" % (self.player, self.player_total)
        print "Dealer has %s showing." % (self.dealer[:2],)
    
    def player_options(self):
        self.screen.blit(self.table,(0,0))
        pygame.display.flip()
        self.show()
        if self.player_total == 21 and self.dealer_total != 21:
            print "BlackJack!! -- Player Wins!! %s" % (self.player,)
            self.play_again()
            return
        if self.dealer_total == 21 and self.dealer_total != 21:
            print "BlackJack!! -- Dealer Wins!! %s" % (self.dealer,)
            self.play_again()
            return
        if self.player_total == 21 and self.dealer_total == 21:
            print "PUSH! Double BlackJack"
            self.play_again()
            return
        choice = raw_input("Do you want to Hit or Stand?: ")
        while choice.lower() != "hit" and choice.lower() != "stand":
            choice = raw_input("Do you want to Hit or Stand?: ")
        while choice.lower() == "hit" and self.player_total <= 21:
            self.player += self.deck.pop(0)
            self.score()
            if self.player_total > 21:
                break
            print "Player has %s and with total %d." % (self.player,self.player_total)
            choice = raw_input("Do you want to Hit or Stand?: ")
        if self.player_total > 21:
            print "Player hand %s, total %d --- Bust!!" % (self.player, self.player_total)
            print "Dealer Wins!"            
        if choice.lower() == 'stand':
            while self.dealer_total < 17:
                self.dealer += self.deck.pop(0)
                self.score()
                if self.dealer_total > 21:
                    print "Dealer hand %s, total %d --- Bust!!" % (self.dealer, self.dealer_total)
                    print "Player Wins!"
                    self.play_again()
                    return
            print "Player Hand/Score: %s %d" % (self.player, self.player_total)
            print "Dealer Hand/Score: %s %d" % (self.dealer, self.dealer_total)
            if self.player_total > self.dealer_total:
                print "Player Wins!!"
            if self.dealer_total > self.player_total:
                print "Dealer Wins!!"
            elif self.dealer_total == self.player_total:
                print "Draw"
        self.play_again()

    def play_again(self):
        game = raw_input("Play again? ")
        while game.lower() != 'yes' and game.lower() != 'no':
            game = raw_input("Play again, yes or no? -- ") 
        if game.lower() == 'yes':
            Blackjack().player_options()
        if game.lower() == 'no':
            return

Blackjack().player_options()



## 'Ace' can be 1 or 11 ---- add that in ##
## hand will be dealt and option to hit or stand even if dealer has blackjack and when it comes out there is not a declaring ## ##"blackjack" ##
## pygame screen x,y (x = 50-700, y = 30-500) ##

