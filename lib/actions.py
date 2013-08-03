import random
import itertools


SUITS = ['heart','diamond','spade','club'] * 13
CARDS = {'deuce':2, 'three':3, 'four':4, 'five':5,
         'six':6, 'seven':7, 'eight':8,'nine':9, 'ten':10, 
         'jack':10, 'queen':10, 'king':10, 'ace':11}

def deal():
    deck = list(itertools.izip(SUITS, CARDS.keys() * 4)) * 6
    random.shuffle(deck)
    player = deck.pop(0) + deck.pop(1)
    dealer = deck.pop(0)       
    return deck

def take():
    deck = deal()
    card = deck[0]
    deck.pop(0) 
    return card


def total(score):
    amount = 0
    for i in score:
        if CARDS.has_key(i):
            amount += CARDS[i]
    if amount > 21 and 'ace' in score:
        for i in range(score.count('ace')):
            if amount > 21:
                amount -= 10
    return amount

def hold(score):
    comp = total(score)
    if comp > 16:
        return    
    if comp < 17:
        card = deck[0]
        deck.pop(0)
        return card
