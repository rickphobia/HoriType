import pygame 

class PrepMsg:
    def __init__(self, tg):
        self.screen = tg.screen
        self.settings = tg.settings
        self.font = pygame.font.Font(None, 50)
        # We do NOT calculate cx/cy here. 
        # The screen might report size (0,0) during startup.

    # --- HELPER: Get Center Dynamically ---
    def get_center(self):
        rect = self.screen.get_rect()
        return rect.centerx, rect.centery

    def game_ends(self):
        cx, cy = self.get_center()
        word = 'Game Ends'
        self._display_msg(word, cx - 100, cy - 200)

    def show_word_count(self, word_count):
        cx, cy = self.get_center()
        msg = f"You have killed {word_count} words"
        self._display_msg(msg, cx - 150, cy - 150)

    def show_wpm(self, word_count, duration):
        cx, cy = self.get_center()
        
        # FIX: WPM = Words Per Minute (60,000 ms)
        # Prevent division by zero crash
        if duration < 1000: 
            minutes = 1 
        else:
            minutes = duration / 60000 
            
        if minutes == 0: minutes = 1
        
        wpm = int(word_count / minutes)
        msg = f"Your WPM is {wpm}"
        self._display_msg(msg, cx - 100, cy - 100)

    def show_start_button(self):
        cx, cy = self.get_center()
        word = 'START'
        # Draw exactly near the middle
        self._display_msg(word, cx - 50, cy - 50)
        
    def show_settings(self):
        cx, cy = self.get_center()
        word = 'SETTINGS'
        self._display_msg(word, cx - 70, cy)

    def show_max_health(self, max_health):
        cx, cy = self.get_center()
        word = f'Max Health = {max_health}'
        self._display_msg(word, cx - 100, cy + 100)

    def show_word_speed(self, word_speed):
        cx, cy = self.get_center()
        word = f"Word speed = {word_speed}"
        self._display_msg(word, cx - 100, cy + 50)
    
    def _display_msg(self, msg, pos_x, pos_y, color=(255, 0, 0)):
        self.image = self.font.render(msg, True, color)
        self.rect = self.image.get_rect()
        # Explicitly set the top-left position
        self.rect.topleft = (pos_x, pos_y)
        self.screen.blit(self.image, self.rect)