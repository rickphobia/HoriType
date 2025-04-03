import pygame
from input import Input 
from settings import Settings
from prep_word import PrepMsg
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

    

    def _start_end_screen(self):
        if self.settings.word_count > 0:
            self.prep_word.game_ends()
            self.prep_word.show_word_count(self.settings.word_count)
            self.prep_word.show_wpm(self.settings.word_count,self.duration)
            print(self.duration)
        self.prep_word.show_start_button()
        self.prep_word.show_settings()


    def _update_screen(self):
        self.dt = self.clock.tick(60)/1000

        self.screen.fill((0,0,0))
        if self.settings.game_active:
            self.k_input._update_text()
            self.duration = pygame.time.get_ticks()
        if not self.settings.game_active:
            self._start_end_screen()

            if self.settings.go_settings:
                self.prep_word.show_word_speed(self.settings.word_speed)
        self._update_input()
        self.k_input._reaching_right()
        pygame.display.flip()
if __name__ == '__main__':
    tg = HoriType()
    tg.run_game()
