import pygame
import time
import os


PATH = os.getcwd() + '/images/'

class GameDisplay(object):
    
    def __init__(self):

        pygame.init()
        pygame.mouse.set_visible(1)
        self.screen = pygame.display.set_mode((800, 600))
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
        self.table = pygame.image.load(PATH + 'new.png')
        self.table.convert_alpha()
        self.banner = pygame.image.load(PATH + 'banner.png')
        self.banner.convert_alpha()
        self.decoration = pygame.image.load(PATH + 'start.png')
        self.decoration.convert_alpha()
        self.edge = pygame.image.load(PATH + 'edge.png')
        self.edge.convert_alpha()
     
    def default_scr(self):
        self.positions = {'1':[50, 240], '2':[230, 360], '3':[460, 280]}
        self.dspot_x = 290
        self.screen.blit(self.backdrop, (0, 0))
        self.screen.blit(self.table, (0, 50))
        self.screen.blit(self.banner, (205, 505))
        self.screen.blit(self.decoration, (565, 150))
        self.stand = self.screen.blit(self.stand_btn, (630, 420))
        time.sleep(0.1)
        self.deal = self.screen.blit(self.deal_btn, (690, 380))
        self.hit = self.screen.blit(self.hit_btn, (562, 445))
        pygame.display.flip()

    def display_hands(self, player_hands): 
        for pl in player_hands:
            for card in player_hands[pl][:2]:
                show_card = pygame.image.load(PATH + card)
                show_card.convert_alpha()
                self.screen.blit(show_card, (self.positions[pl][0],
                                             self.positions[pl][1]))
                self.positions[pl][0] += 30 
        pygame.display.flip()

    def display_card(self, card_msg):
        player = card_msg.keys()[0]
        card = ''.join(i for i in card_msg[player])
        card = pygame.image.load(PATH + card)
        card.convert_alpha()
        self.screen.blit(card, (self.positions[player][0], 
                               self.positions[player][1]))
        self.positions[player][0] += 30
        pygame.display.flip()

    def display_dealer(self, card):
        self.screen.blit(self.edge, (332, 100))
        card = pygame.image.load(PATH + card)
        card.convert_alpha()
        self.screen.blit(card, (260, 100))
        pygame.display.flip()

    def display_dealer_take(self, card):
        card = pygame.image.load(PATH + card[0])
        card.convert_alpha()
        self.screen.blit(card, (self.dspot_x, 100))
        self.dspot_x += 30
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
        self.screen.blit(btn_click, (632, 422))
        pygame.display.flip()

    def stand_unclick(self):
        self.screen.blit(self.stand_btn, (630, 420))
        pygame.display.flip()
    
    def hit_click(self):
        btn_click = pygame.transform.scale(self.hit_btn, (65, 63))
        self.screen.blit(btn_click, (564, 447))
        pygame.display.flip()

    def hit_unclick(self):
        self.screen.blit(self.hit_btn, (562, 445))
        pygame.display.flip()

    def deal_click(self):
        btn_click = pygame.transform.scale(self.deal_btn, (65, 63))
        self.screen.blit(btn_click, (692, 383))
        pygame.display.flip()

    def deal_unclick(self):
        self.screen.blit(self.deal_btn, (690, 380))
        pygame.display.flip()

    def exit(self):
        pygame.display.quit()

