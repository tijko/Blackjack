import random
import itertools


class Shuffle(object):
    """
    Class for setting up the deck and 
    accessing cards.
    """
    def __init__(self):
        self.suits = ['heart','diamond','spade','club'] * 13
        self.cards = {'deuce':2,'three':3,'four':4,'five':5,'six':6,'seven':7,
                      'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
        # creates a six deck with the suits and cards variables # 
        self.deck = list(itertools.izip(self.suits,self.cards.keys() * 4)) * 6
        # shuffles the decks to randomize them #
        random.shuffle(self.deck)
        return


class Deal(Shuffle):
    """
    Class that handles passing cards to dealer or
    player when called.
    """ 
    def __init__(self):
        Shuffle.__init__(self)
        # when Deal class is called the player hand pops the first two of the deck #
        self.player = self.deck.pop(0) + self.deck.pop(1)
        # Just one for the dealer hand #
        self.dealer = self.deck.pop(0)       


class Take(Shuffle):
    """
    Class for 'hit'ing a player/dealer
    when asked for.
    """
    def card(self):
        # when 'hit' button is clicked pygames events trigger Take() #
        # player grabs first #
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
            # Total() takes the hands 'cards' and matches the key in the deck #
            if self.cards.has_key(i):
                self.amount += self.cards[i]
        # This conditional will check for the best possible hand with aces #
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
        # blackjack rules dealer must take cards while under 17 #
        if comp > 16:
            return    
        if comp < 17:
            self.card = self.deck[0]
            self.deck.pop(0)
            return self.card

