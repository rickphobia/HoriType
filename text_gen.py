import random 
from random import randint 
import pygame 
from pygame.math import Vector2 
from pygame.sprite import Sprite
class Gen_Ran_Word(Sprite):
    def __init__(self,tg,ran_word,color = (255,255,255)):
        super().__init__()
        # filepath = 'database.txt'
        # with open(filepath) as fp:
        #     self.wordlist = [word.strip() for word in fp.readlines()]
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tg.settings
        self.font = pygame.font.SysFont(None, 50)
        self.word = ran_word
        # ran_word = random.choice(self.wordlist)
        self.image = self.font.render(self.word, True, color)
        self.rect = self.image.get_rect()
        self.rect.y = randint(10,1000)
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.word_speed
        self.rect.x = self.x
        # collision = pygame.sprite.spritecollideany(self.rect,self.screen_rect.right)
        # if collision: 
        #     self.settings.game_active = False 
            
