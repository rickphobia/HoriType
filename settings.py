import pygame 

class Settings:
    def __init__(self):
        pygame.init()
        self.word_speed_const  = 5
        self.word_speed = self.word_speed_const
        self.word_count = 0
        self.game_active = False
        self.go_settings = False
        self.max_health = 3 
        self.reaching_right = True 
        self.gen_move_text =True 
        self.word_speed_slowdown = 0.1
        self.invincible = False
        self.invincible_active = False

        self.clear = False
        self.dir = +1 
        self.reverse = False 
        self.reverse_active = False 

        self.time_slow = False 
        self.time_slow_active  = False 

        self.freeze = False 
        self.freeze_active  = False 

        self.invincible_duration = 3000
        self.timeslow_duration = 3000
        self.reverse_duration = 3000
        self.freeze_duration = 4000

    def initialize_stats(self):
        self.reverse_active = False 
        self.time_slow_active  = False 
        self.freeze_active  = False 
        self.reaching_right = True 
        self.invincible_active = False
        
        self.health_remain = self.max_health
        self.word_count = 0
        self.invincible = False
        self.clear = False
        self.reverse = False 
        self.time_slow = False 
        self.freeze = False 