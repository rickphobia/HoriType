import pygame

class Settings:
    def __init__(self):
        pygame.init()
        self.word_speed_const  = 5
        self.word_speed = int(self.word_speed_const)
        self.word_count = 0
        # which screen is showing: 'menu', 'settings', 'playing' or 'over'
        self.state = 'menu'
        # the screen 'back' returns to from settings
        self.prev_state = 'menu'
        # 'normal', or 'super' where every power up is ready at the start
        self.mode = 'normal'
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
        self.word_rates = {'slow': 1000, 'normal': 700, 'fast': 450}
        self.word_rate = 'normal'
        self.word_interval = self.word_rates[self.word_rate]
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
        self.game_time = 0

        # words die when their right edge reaches this many pixels from the right of the screen
        self.death_margin = 60

    @property
    def game_active(self):
        return self.state == 'playing'

    def wpm(self):
        # words typed per minute of play; count at least 5 seconds so the first word doesn't read as 600 wpm
        minutes = max(self.game_time, 5000) / 60000
        return int(self.word_count / minutes)


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
        if self.mode == 'super':
            for name in self.powersup_colors:
                setattr(self, name, True)
        self.game_start = pygame.time.get_ticks()
        self.game_time = 0
