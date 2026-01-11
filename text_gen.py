from random import randint 
import pygame 
from pygame.sprite import Sprite
class Gen_Ran_Word(Sprite):
    def __init__(self,tg,ran_word,color = (255,255,255)):
        super().__init__()
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        max_y = self.screen_rect.height - 100 
        self.settings = tg.settings
        self.font = pygame.font.SysFont(None, 50)
        self.word = ran_word
        self.image = self.font.render(self.word, True, color)
        self.rect = self.image.get_rect()
        self.rect.y = randint(10,max_y)
        self.x = float(self.rect.x)
        

    def update(self):
        self.x += self.settings.word_speed * self.settings.dir
        self.rect.x = self.x

