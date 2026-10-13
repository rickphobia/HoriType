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
        self.font = pygame.font.Font(None, 50)
        self.color = ((255,255,255))
        self.line_color = (45, 45, 45)
        self.user_input = []
        self.k_input = Input(self,self.user_input)
        self.health = Health(self)
        self.duration = 0
        self.game_running = True

    async def run_game(self):
        while self.game_running:
            if self.k_input._key_input() is None:
                self.game_running = False
                break
            self._update_screen()
            await asyncio.sleep(0)
        pygame.quit()



    def _update_input(self):
        # typed text sits right-aligned in the bottom hud, clear of the hearts on the left
        user_list = ''.join(self.user_input)
        self.msg_image = self.font.render('> ' + user_list, True, self.color)
        self.msg_rect = self.msg_image.get_rect()
        margin_x = 40
        self.msg_rect.midright = (
            self.screen_rect.right - margin_x,
            self.screen_rect.bottom - self.settings.hud_height // 2
        )

        self.screen.blit(self.msg_image, self.msg_rect)

    def _draw_layout(self):
        # thin lines mark the top power up bar and the bottom hud; words only move between them
        top = self.settings.top_bar_height
        bottom = self.screen_rect.height - self.settings.hud_height
        pygame.draw.line(self.screen, self.line_color, (0, top), (self.screen_rect.right, top))
        pygame.draw.line(self.screen, self.line_color, (0, bottom), (self.screen_rect.right, bottom))

    def _start_end_screen(self):
        lines = []
        if self.settings.word_count > 0:
            lines.append(self.prep_word.game_ends())
            lines.append(self.prep_word.show_word_count(self.settings.word_count))
            lines.append(self.prep_word.show_wpm(self.settings.word_count,self.duration))
        lines.append(self.prep_word.show_start_button())
        lines.append(self.prep_word.show_settings())
        if self.settings.go_settings:
            lines.append(self.prep_word.show_word_speed(self.settings.word_speed_const))
            lines.append(self.prep_word.show_word_speed_hint())
            lines.append(self.prep_word.show_max_health(self.settings.max_health))
            lines.append(self.prep_word.show_max_health_hint())
        lines.append(self.prep_word.show_hint())
        self.prep_word.draw_menu(lines)


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
            now = pygame.time.get_ticks()
            self.duration = now - self.settings.game_start
            self._powersup_times('invincible_active', 'invincible', 'invincible_start', 'invincible_duration', 'reaching_right', False, True)
            self._powersup_times('reverse_active', 'reverse', 'reverse_start', 'reverse_duration', 'dir', -1, 1 )
            self._powersup_times('timeslow_active', 'timeslow', 'timeslow_start', 'timeslow_duration', 'word_speed', 0.1, "word_speed_const")
            self._powersup_times('freeze_active', 'freeze', 'freeze_start', 'freeze_duration', 'gen_move_text', False, True)
            self._draw_layout()
            self.k_input._update_text()
            self.k_input._reaching_right()
            self.prep_word.draw_powerups(now)
            self.health.blitme()

        if not self.settings.game_active:
            self._start_end_screen()

        self._update_input()
        pygame.display.flip()
# ... (End of HoriType class) ...

# Define the main entry point (Required for Web)
async def main():
    tg = HoriType()
    await tg.run_game()

if __name__ == '__main__':
    # This block runs on your Laptop
    asyncio.run(main())
