import pygame
import asyncio
from input import Input 
from settings import Settings
from prep_word import PrepMsg
from health import Health
class HoriType:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.prep_word = PrepMsg(self)
        self.width_ctr = self.prep_word.width_center  
        self.font = pygame.font.Font(None, 50)
        self.color = ((255,255,255))
        self.user_input = [] 
        self.k_input = Input(self,self.user_input)
        self.FIVESEC = pygame.USEREVENT+1
        pygame.time.set_timer(self.FIVESEC, 700)
        self.user_input = self.k_input._key_input()
        self.health = Health(self)
        self.game_running = True 

    async def run_game(self):
        while self.game_running:
            self.k_input._key_input() 
            self._update_screen()
            await asyncio.sleep(0)

            
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

    def _showing_powers_up_(self,powerups,emoji,pos_x, pos_y,color):
        if powerups:
            self.prep_word._display_msg(emoji,pos_x,pos_y,color)
    def showing_clear(self):
        self._showing_powers_up_(self.settings.clear,'*', self.width_ctr, 5, (255,215,0))

    def showing_invincible(self):
        self._showing_powers_up_(self.settings.invincible,'*', self.width_ctr-15, 5, (200,65,65))

    def showing_timeslow(self):
        self._showing_powers_up_(self.settings.timeslow,'*', self.width_ctr+15, 5, (225,235,237))
    
    def showing_freeze(self):
        self._showing_powers_up_(self.settings.freeze,'*', self.width_ctr+10, 5, (147,249,255))

    def showing_reverse(self):
        self._showing_powers_up_(self.settings.reverse,'*', self.width_ctr-10, 5, (0,255,0))
    def _start_end_screen(self):
        if self.settings.word_count > 0:
            self.prep_word.game_ends()
            self.prep_word.show_word_count(self.settings.word_count)
            self.prep_word.show_wpm(self.settings.word_count,self.duration)
            # print(self.duration)
        self.prep_word.show_start_button()
        self.prep_word.show_settings()


#use chatgpt to help and just know getattr and setattr
# why getattr, and setattr, because normal attr doesnt change the real attr only changes the onpy
#getattr and setattr changes the attr fundamentally
    def _powersup_times(self,active_attr,powerup_attr,start_attr,duration_attr,effect_attr,effect_on, effect_off):
        if getattr(self.settings, active_attr):
            current_time = pygame.time.get_ticks()
            start_time = getattr(self.settings, start_attr)
            duration = getattr(self.settings, duration_attr)
            if current_time - start_time >= duration:
                setattr(self.settings, powerup_attr, False)
                setattr(self.settings,active_attr, False)

            else: 
                setattr(self.settings, effect_attr, effect_on)
        else:
            #cuz computer dk word_speed_const is a reference str, so u have to set value from the word speed const and use it 
            if isinstance(effect_off,str):
                offvalue = getattr(self.settings, effect_off)
            else:
                offvalue = effect_off
            setattr(self.settings, effect_attr, offvalue)

    def _update_screen(self):
        self.dt = self.clock.tick(60)/1000
        # pygame.mouse.set_visible(False)

        self.screen.fill((0,0,0))
        if self.settings.game_active:
            self.k_input._update_text()
            self.duration = pygame.time.get_ticks()
            self.showing_clear()
            self.showing_invincible()
            self.showing_freeze()
            self.showing_reverse()
            self.showing_timeslow()
            self._powersup_times('invincible_active', 'invincible',  'invincible_start', 'invincible_duration','reaching_right', False, True)
            self._powersup_times('reverse_active', 'reverse', 'reverse_start','reverse_duration', 'dir', -1, 1 )
            self._powersup_times('timeslow_active', 'timeslow', 'timeslow_start', 'timeslow_duration', 'word_speed', 0.1, "word_speed_const")
            self._powersup_times('freeze_active', 'freeze', 'freeze_start', 'freeze_duration', 'gen_move_text',False,True)
            self.health.blitme()

        if not self.settings.game_active:
            self._start_end_screen()

            if self.settings.go_settings:
                self.prep_word.show_word_speed(self.settings.word_speed_const)
                self.prep_word.show_max_health(self.settings.max_health)
        self._update_input()
        self.k_input._reaching_right()
        pygame.display.flip()
# ... (End of HoriType class) ...

# Define the main entry point (Required for Web)
async def main():
    tg = HoriType()
    await tg.run_game()

if __name__ == '__main__':
    # This block runs on your Laptop
    asyncio.run(main())