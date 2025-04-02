import pygame 

class Settings:
    def __init__(self):
        pygame.init()
        self.word_speed = 5
        self.word_count = 0
        self.game_active = False
        self.go_settings = False
        
    def initialize_stats(self):
        self.word_count = 0