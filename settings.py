import pygame

class Settings:
    def __init__(self):
        pygame.init()
        self.word_speed_const  = 5
        self.word_speed = int(self.word_speed_const)
        self.word_count = 0
        self.game_active = False
        self.go_settings = False
        self.max_health = 3
        self.health_remain = self.max_health
        self.reaching_right = True
        self.gen_move_text =True
        self.invincible = False
        self.invincible_active = False

        self.clear = False
        self.reverse = False
        self.reverse_active = False
        self.dir = 1

        self.timeslow= False
        self.timeslow_active  = False

        self.freeze = False
        self.freeze_active  = False

        self.invincible_duration = 3000
        self.timeslow_duration = 3000
        self.reverse_duration = 3000
        self.freeze_duration = 3000
        self.invincible_start = 0
        self.timeslow_start = 0
        self.reverse_start = 0
        self.freeze_start = 0

        # how often (ms) a new word / power up tries to spawn
        self.word_interval = 700
        self.powersup_interval = 2000

        # one colour per power up, used for the falling word and the top bar
        self.powersup_colors = {
            'clear': (255, 215, 0),
            'freeze': (147, 249, 255),
            'reverse': (0, 255, 0),
            'invincible': (200, 65, 65),
            'timeslow': (225, 235, 237),
        }

        # screen layout: words only move between the top bar and the bottom hud
        self.top_bar_height = 50
        self.hud_height = 110
        self.word_font_size = 46
        self.max_input_chars = 24

        # limits for the values typed in the settings screen
        self.min_word_speed, self.max_word_speed = 1, 30
        self.min_health, self.max_health_limit = 1, 10

        self.game_start = 0


    def initialize_stats(self):
        self.reverse_active = False
        self.invincible_start = 0
        self.timeslow_start = 0
        self.reverse_start = 0
        self.freeze_start = 0
        self.timeslow_active  = False
        self.freeze_active  = False
        self.reaching_right = True
        self.gen_move_text = True
        self.dir = 1
        self.word_speed = self.word_speed_const
        self.invincible_active = False

        self.health_remain = self.max_health
        self.word_count = 0
        self.invincible = False
        self.clear = False
        self.reverse = False
        self.timeslow= False
        self.freeze = False
        self.game_start = pygame.time.get_ticks()
