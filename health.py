import pygame
import os 
class Health:
    def __init__(self,ht):
        pygame.init()
        self.screen = ht.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ht.settings
        health_path= "images/health.bmp"
        empty_health_path= "images/empty_health.bmp"
        self.health = pygame.image.load(health_path)
        self.health = pygame.transform.scale(self.health,(70,70))

        self.empty_health = pygame.image.load(empty_health_path)
        self.empty_health = pygame.transform.scale(self.empty_health,(70,70))
        
        self.health_rect = self.health.get_rect()
        self.empty_health_rect = self.empty_health.get_rect()

    def blitme(self):
        spacing = 70
        for i in range(self.settings.max_health):
            x_pos = self.health_rect.width + spacing*i
            y_pos = self.screen.get_height() - 100
            if i < self.settings.health_remain: 
                self.screen.blit(self.health, (x_pos, y_pos))
            else: 
                self.screen.blit(self.empty_health, (x_pos,y_pos))
