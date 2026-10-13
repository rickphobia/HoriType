import pygame

class PrepMsg:
    def __init__(self, tg):
        self.screen = tg.screen
        self.settings = tg.settings
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 32)
        self.title_color = (255, 0, 0)
        self.text_color = (255, 0, 0)
        self.hint_color = (140, 140, 140)
        # We do NOT calculate cx/cy here.
        # The screen might report size (0,0) during startup.

    # --- HELPER: Get Center Dynamically ---
    def get_center(self):
        rect = self.screen.get_rect()
        return rect.centerx, rect.centery

    def game_ends(self):
        return ('Game Ends', self.font, self.title_color)

    def show_word_count(self, word_count):
        return (f"You have killed {word_count} words", self.font, self.text_color)

    def show_wpm(self, word_count, duration):
        # WPM = Words Per Minute (60,000 ms); count at least one second so a quick ESC can't divide by zero
        minutes = max(duration, 1000) / 60000
        wpm = int(word_count / minutes)
        return (f"Your WPM is {wpm}", self.font, self.text_color)

    def show_start_button(self):
        return ('START', self.font, self.text_color)

    def show_settings(self):
        return ('SETTINGS', self.font, self.text_color)

    def show_hint(self):
        return ('type a word and press Enter', self.small_font, self.hint_color)

    def show_word_speed(self, word_speed):
        return (f"Word speed = {word_speed}", self.font, self.text_color)

    def show_word_speed_hint(self):
        s = self.settings
        return (f"type 'word speed {s.min_word_speed}-{s.max_word_speed}'", self.small_font, self.hint_color)

    def show_max_health(self, max_health):
        return (f'Max Health = {max_health}', self.font, self.text_color)

    def show_max_health_hint(self):
        s = self.settings
        return (f"type 'max health {s.min_health}-{s.max_health_limit}'", self.small_font, self.hint_color)

    def draw_menu(self, lines, gap=12):
        # stack the lines in a centred column above the bottom hud, so nothing overlaps
        # whatever the text length or how many lines are shown
        lines = [line for line in lines if line]
        images = [font.render(text, True, color) for text, font, color in lines]
        total = sum(image.get_height() for image in images) + gap * (len(images) - 1)
        rect = self.screen.get_rect()
        area_bottom = rect.height - self.settings.hud_height
        y = max(self.settings.top_bar_height, (area_bottom - total) // 2)
        for image in images:
            image_rect = image.get_rect(midtop=(rect.centerx, y))
            self.screen.blit(image, image_rect)
            y += image_rect.height + gap

    def draw_powerups(self, now):
        # held power ups sit side by side in the top bar; active ones show their time left
        items = []
        for name, color in self.settings.powersup_colors.items():
            if not getattr(self.settings, name):
                continue
            label = name
            if getattr(self.settings, f'{name}_active', False):
                start = getattr(self.settings, f'{name}_start')
                duration = getattr(self.settings, f'{name}_duration')
                left = max(0, duration - (now - start))
                label = f'{name} {left / 1000:.1f}s'
            items.append(self.small_font.render(label, True, color))
        if not items:
            return
        spacing = 30
        total = sum(image.get_width() for image in items) + spacing * (len(items) - 1)
        rect = self.screen.get_rect()
        x = rect.centerx - total // 2
        for image in items:
            self.screen.blit(image, image.get_rect(midleft=(x, self.settings.top_bar_height // 2)))
            x += image.get_width() + spacing

    def _display_msg(self, msg, pos_x, pos_y, color=(255, 0, 0)):
        self.image = self.font.render(msg, True, color)
        self.rect = self.image.get_rect()
        # Explicitly set the top-left position
        self.rect.topleft = (pos_x, pos_y)
        self.screen.blit(self.image, self.rect)
