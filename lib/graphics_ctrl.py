import pygame
import time
import os
from collections import defaultdict

PATH = os.getcwd() + '/images/'
os.environ['SDL_VIDEO_WINDOW_POS'] = '170, 30'

class GameDisplay(object):
    
    def __init__(self):
        pygame.init() 
        pygame.mouse.set_visible(1)
        self.screen = pygame.display.set_mode((800, 600))
        self.player_data = defaultdict(list)
        self.dealer_data = list()
        self.bust = pygame.image.load(PATH + 'bust.png')
        self.bust.convert_alpha()
        self.dealer_bj = pygame.image.load(PATH + 'dealer_blackjack.png')
        self.dealer_bj.convert_alpha()
        self.player_bj = pygame.image.load(PATH + 'player_blackjack.png')
        self.player_bj.convert_alpha()
        self.dealer_wins = pygame.image.load(PATH + 'dealer_wins.png')
        self.dealer_wins.convert_alpha()
        self.player_wins = pygame.image.load(PATH + 'player_wins.png')
        self.player_wins.convert_alpha()
        self.tie = pygame.image.load(PATH + 'tie.png')
        self.tie.convert_alpha()
        self.stand_btn = pygame.image.load(PATH + 'stand.png')
        self.stand_btn.convert_alpha()
        self.deal_btn = pygame.image.load(PATH + 'deal.png')
        self.deal_btn.convert_alpha()
        self.hit_btn = pygame.image.load(PATH + 'hit.png')
        self.hit_btn.convert_alpha()
        self.backdrop = pygame.image.load(PATH + 'black.jpg')
        self.backdrop.convert_alpha()
        self.table = pygame.image.load(PATH + 'table.png')
        self.table.convert_alpha()
        self.decoration = pygame.image.load(PATH + 'start.png')
        self.decoration.convert_alpha()
        self.edge = pygame.image.load(PATH + 'edge.png')
        self.edge.convert_alpha()
        self.cardtray = pygame.image.load(PATH + 'cardtray.png')
        self.cardtray.convert_alpha()
        self.blue = pygame.image.load(PATH + 'blue.png')
        self.blue.convert_alpha()
        self.red = pygame.image.load(PATH + 'red.png')
        self.red.convert_alpha()
        self.green = pygame.image.load(PATH + 'green.png')
        self.green.convert_alpha()
        self.circle = pygame.image.load(PATH + 'position.png')
        self.circle.convert_alpha()
        self.turn = pygame.image.load(PATH + 'turn.png')
        self.turn.convert_alpha()
        self.tablemsg = pygame.image.load(PATH + 'tablemsg.png')
        self.tablemsg.convert_alpha()
        self.options = pygame.image.load(PATH + 'options.png')
        self.options.convert_alpha()

    def default_scr(self):  
        self.positions = {'1':[40, 230], '2':[235, 320], '3':[450, 320], '4':[645, 250]} 
        bet_positions = [(60, 315), (255, 405), (470, 405), (665, 335)]
        self.dspot_x = 310 
        self.screen.blit(self.backdrop, (0, 0))
        self.screen.blit(self.table, (-145, 0))
        self.screen.blit(self.tablemsg, (205, 175))
        self.screen.blit(self.options, (205, 495))
        self.screen.blit(self.cardtray, (595, 5)) 
        self.stand = self.screen.blit(self.stand_btn, (450, 515)) 
        time.sleep(0.1)
        self.deal = self.screen.blit(self.deal_btn, (365, 515)) 
        self.hit = self.screen.blit(self.hit_btn, (280, 515)) 
        for pos in bet_positions:
            self.screen.blit(self.circle, (pos[0], pos[1]))
        pygame.display.flip()

    def display_hands(self, player_hands, turn=None): 
        for pl in player_hands:
            for card in player_hands[pl]:
                if not turn:
                    self.player_data[pl].append(card)
                show_card = pygame.image.load(PATH + card)
                show_card.convert_alpha()
                self.screen.blit(show_card, (self.positions[pl][0],
                                             self.positions[pl][1]))
                self.positions[pl][0] += 20 
        pygame.display.flip()

    def display_card(self, card_msg):
        player = card_msg.keys()[0]
        card = ''.join(i for i in card_msg[player])
        self.player_data[str(player)].append(card)
        card = pygame.image.load(PATH + card)
        card.convert_alpha()
        self.screen.blit(card, (self.positions[player][0], 
                                self.positions[player][1]))
        self.positions[player][0] += 20
        pygame.display.flip()

    def display_dealer(self, card):
        self.dealer_data.append(card)
        self.screen.blit(self.edge, (352, 70)) 
        card = pygame.image.load(PATH + card)
        card.convert_alpha()
        self.screen.blit(card, (280, 70)) 
        pygame.display.flip()

    def display_dealer_take(self, card):
        card = pygame.image.load(PATH + card[0])
        card.convert_alpha()
        self.screen.blit(card, (self.dspot_x, 70)) 
        self.dspot_x += 30
        pygame.display.flip()

    def display_turn(self, turn):
        self.default_scr() 
        self.display_dealer(self.dealer_data[0])
        self.display_hands(self.player_data, turn=True)
        turn_positions = {1:(15, 230), 2:(210, 320), 3:(415, 320), 4:(620, 250)}  
        pos = turn_positions[turn]
        self.screen.blit(self.turn, pos)
        pygame.display.flip()

    def dealer_blackjack(self):
        self.screen.blit(self.dealer_bj, (200, 200)) 
        pygame.display.flip()

    def player_blackjack(self):
        self.screen.blit(self.player_bj, (200, 200)) 
        pygame.display.flip()

    def dealer_win(self):
        self.screen.blit(self.dealer_wins, (260, 200)) 
        pygame.display.flip()

    def player_win(self):
        self.screen.blit(self.player_wins, (250, 200)) 
        pygame.display.flip()

    def player_bust(self):
        self.screen.blit(self.bust, (150, 200)) 
        pygame.display.flip()

    def tie_game(self):
        self.screen.blit(self.tie, (250, 200)) 
        pygame.display.flip()

    def stand_click(self):
        btn_click = pygame.transform.scale(self.stand_btn, (65, 63))
        self.screen.blit(btn_click, (452, 517)) 
        pygame.display.flip()

    def stand_unclick(self):
        self.screen.blit(self.stand_btn, (450, 515)) 
        pygame.display.flip()
    
    def hit_click(self):
        btn_click = pygame.transform.scale(self.hit_btn, (65, 63)) 
        self.screen.blit(btn_click, (282, 517)) 
        pygame.display.flip()

    def hit_unclick(self):
        self.screen.blit(self.hit_btn, (280, 515)) 
        pygame.display.flip()

    def deal_click(self):
        btn_click = pygame.transform.scale(self.deal_btn, (65, 63))
        self.screen.blit(btn_click, (367, 517)) 
        pygame.display.flip()

    def deal_unclick(self):
        self.screen.blit(self.deal_btn, (365, 515)) 
        pygame.display.flip()

    def exit(self):
        pygame.display.quit()

