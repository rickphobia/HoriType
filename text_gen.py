import pygame
from pygame.sprite import Sprite
class Gen_Ran_Word(Sprite):
    def __init__(self,tg,ran_word,lane,lane_y,color = (255,255,255)):
        super().__init__()
        self.settings = tg.settings
        self.word = ran_word
        self.lane = lane
        self.image = tg.word_font.render(self.word, True, color)
        self.rect = self.image.get_rect()
        # start just off the left edge so the word slides in instead of popping up
        self.rect.right = 0
        self.rect.y = lane_y
        self.x = float(self.rect.x)


    def update(self):
        self.x += self.settings.word_speed * self.settings.dir
        self.rect.x = self.x
