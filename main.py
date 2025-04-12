import pygame
from input import Input 
from settings import Settings
from prep_word import PrepMsg
from health import Health
class HoriType:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.prep_word = PrepMsg(self)
        self.font = pygame.font.SysFont(None, 50)
        self.color = ((255,255,255))
        self.user_input = [] 
        self.k_input = Input(self,self.user_input)
        self.FIVESEC = pygame.USEREVENT+1
        pygame.time.set_timer(self.FIVESEC, 700)
        self.user_input = self.k_input._key_input()
        self.health = Health(self)

    def run_game(self):
        while True:
            self.k_input._key_input() 
            self._update_screen()

            
    def _update_input(self):
        user_list = ''.join(self.user_input)
        self.msg_image = self.font.render(str(user_list), True, self.color)
        self.msg_rect = self.msg_image.get_rect()
        margin_x = 100
        margin_y = 100
        self.msg_rect.bottomright = (
            self.screen_rect.right - margin_x,
            self.screen_rect.bottom - margin_y
        )
        
        self.screen.blit(self.msg_image, self.msg_rect)
    # def _settings_scene(self):

    def showing_powers_up_(self):
        if self.settings.clear:
            self.prep_word._display_msg('*',self.prep_word.width_center, 5, (255,215,0))
        if self.settings.invincible:
            self.prep_word._display_msg('*',self.prep_word.width_center-15, 5, (200,65,45))
        if self.settings.time_slow:
            self.prep_word._display_msg('*',self.prep_word.width_center+15, 5, (225,235,237))
        if self.settings.freeze:
            self.prep_word._display_msg('*',self.prep_word.width_center+10, 5, (147,249,255))
        if self.settings.reverse:
            self.prep_word._display_msg('*',self.prep_word.width_center-10, 5, (0,255,0))
    def _start_end_screen(self):
        if self.settings.word_count > 0:
            self.prep_word.game_ends()
            self.prep_word.show_word_count(self.settings.word_count)
            self.prep_word.show_wpm(self.settings.word_count,self.duration)
            print(self.duration)
        self.prep_word.show_start_button()
        self.prep_word.show_settings()

    def _freeze_times (self):
        if self.settings.freeze_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.k_input.freeze_start >= self.settings.freeze_duration:
                self.settings.freeze_active = False
                self.settings.freeze = False
            else:
                self.settings.gen_move_text = False

        else:
            self.settings.gen_move_text = True 

    def _timeslow_times(self):
        if self.settings.time_slow_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.k_input.time_slow_start >= self.settings.timeslow_duration:
                self.settings.time_slow_active = False
                self.settings.time_slow = False

            else:
                self.settings.word_speed = self.settings.word_speed_slowdown 

        else:
            self.settings.word_speed = self.settings.word_speed_const


    def _reverse_times(self):
        if self.settings.reverse_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.k_input.reverse_start >= self.settings.reverse_duration:
                self.settings.reverse = False
                self.settings.reverse_active = False 

            else:
                self.settings.dir = -1

        else: 
            self.settings.dir = 1 




    def _invincible_times(self):
        if self.settings.invincible_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.k_input.invincible_start >= self.settings.invincible_duration:
                self.settings.invincible_active = False 
                self.settings.invincible= False 

            else:
                self.settings.reaching_right = False 

        else:
            self.settings.reaching_right= True 

    def _update_screen(self):
        self.dt = self.clock.tick(60)/1000
        pygame.mouse.set_visible(False)

        self.screen.fill((0,0,0))
        if self.settings.game_active:
            self.k_input._update_text()
            self.duration = pygame.time.get_ticks()
            self.showing_powers_up_()
            self._invincible_times()
            self._freeze_times()
            self._timeslow_times()
            self._reverse_times()
            self.health.blitme()
        if not self.settings.game_active:
            self._start_end_screen()

            if self.settings.go_settings:
                self.prep_word.show_word_speed(self.settings.word_speed_const)
                self.prep_word.show_max_health(self.settings.max_health)
        self._update_input()
        self.k_input._reaching_right()
        pygame.display.flip()
if __name__ == '__main__':
    tg = HoriType()
    tg.run_game()
