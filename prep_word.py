import pygame

class PrepMsg:
    def __init__(self, tg):
        self.screen = tg.screen
        self.settings = tg.settings
        self.title_font = pygame.font.Font(None, 96)
        self.font = pygame.font.Font(None, 50)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 32)
        self.title_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.hint_color = (140, 140, 140)
        self.select_color = (60, 15, 15)
        # We do NOT calculate cx/cy here.
        # The screen might report size (0,0) during startup.

    # --- HELPER: Get Center Dynamically ---
    def get_center(self):
        rect = self.screen.get_rect()
        return rect.centerx, rect.centery

    def _text(self, text, font=None, color=None):
        return (font or self.font).render(text, True, color or self.text_color)

    def _rows(self, pairs, selected=None):
        # two column block: command on the left, what it does on the right.
        # settings rows use the big font for both columns and can show one row as selected
        big = selected is not None
        lefts = [self._text(left, self.font, color) for left, _, color in pairs]
        rights = [self._text(right, self.font if big else self.small_font,
                             self.text_color if big else self.hint_color) for _, right, _ in pairs]
        pad, col_gap, row_gap = 16, 30, 8
        left_width = max(image.get_width() for image in lefts)
        width = pad * 2 + left_width + col_gap + max(image.get_width() for image in rights)
        row_height = max(image.get_height() for image in lefts + rights) + pad
        block = pygame.Surface((width, len(pairs) * (row_height + row_gap) - row_gap), pygame.SRCALPHA)
        for i, (left, right) in enumerate(zip(lefts, rights)):
            y = i * (row_height + row_gap)
            if i == selected:
                block.fill(self.select_color, pygame.Rect(0, y, width, row_height))
            block.blit(left, left.get_rect(midleft=(pad, y + row_height // 2)))
            block.blit(right, right.get_rect(midleft=(pad + left_width + col_gap, y + row_height // 2)))
        return block

    def _stats(self, stats):
        # big numbers with a small label underneath, side by side
        blocks = []
        for value, label in stats:
            number = self._text(value, self.big_font)
            name = self._text(label, self.small_font, self.hint_color)
            block = pygame.Surface((max(number.get_width(), name.get_width()), number.get_height() + name.get_height() + 4), pygame.SRCALPHA)
            block.blit(number, number.get_rect(midtop=(block.get_width() // 2, 0)))
            block.blit(name, name.get_rect(midtop=(block.get_width() // 2, number.get_height() + 4)))
            blocks.append(block)
        gap = 70
        surface = pygame.Surface((sum(b.get_width() for b in blocks) + gap * (len(blocks) - 1), max(b.get_height() for b in blocks)), pygame.SRCALPHA)
        x = 0
        for block in blocks:
            surface.blit(block, (x, 0))
            x += block.get_width() + gap
        return surface

    def _commands(self):
        s = self.settings
        return self._rows([
            ('start', 'normal game', self.title_color),
            ('super', 'start with every power up ready', s.powersup_colors['clear']),
            ('settings', f'speed {s.word_speed_const}  ·  health {s.max_health}  ·  rate {s.word_rate}', self.title_color),
        ])

    def show_menu(self):
        self._draw_stack([
            (self._text('HoriType', self.title_font, self.title_color), 10),
            (self._text('type a command and press Enter', self.small_font, self.hint_color), 50),
            (self._commands(), 0),
        ])

    def show_game_over(self, game_time):
        s = self.settings
        seconds = game_time // 1000
        mode = 'super mode' if s.mode == 'super' else 'normal mode'
        self._draw_stack([
            (self._text('Game Over', self.title_font, self.title_color), 10),
            (self._text(mode, self.small_font, self.hint_color), 30),
            (self._stats([
                (str(s.word_count), 'words'),
                (str(s.wpm()), 'wpm'),
                (f'{seconds // 60}:{seconds % 60:02d}', 'time'),
            ]), 50),
            (self._commands(), 16),
            (self._text('Esc for the main menu', self.small_font, self.hint_color), 0),
        ])

    def show_settings(self, selected):
        s = self.settings
        rows = [
            ('Word speed', f'<  {s.word_speed_const}  >'),
            ('Max health', f'<  {s.max_health}  >'),
            ('Word rate', f'<  {s.word_rate}  >'),
        ]
        self._draw_stack([
            (self._text('Settings', self.title_font, self.title_color), 40),
            (self._rows([(name, value, self.text_color) for name, value in rows], selected=selected), 40),
            (self._text('Up / Down to choose     Left / Right to change     Enter or Esc to go back', self.small_font, self.hint_color), 10),
            (self._text("or type:  speed 7   ·   health 5   ·   rate fast", self.small_font, self.hint_color), 0),
        ])

    def _draw_stack(self, items):
        # stack surfaces in a centred column above the bottom hud, so nothing overlaps
        # whatever the text length or how many lines are shown
        total = sum(surface.get_height() + gap for surface, gap in items)
        rect = self.screen.get_rect()
        area_bottom = rect.height - self.settings.hud_height
        y = max(10, (area_bottom - total) // 2)
        for surface, gap in items:
            self.screen.blit(surface, surface.get_rect(midtop=(rect.centerx, y)))
            y += surface.get_height() + gap

    def draw_score(self):
        # live words and wpm in the corners of the top bar
        s = self.settings
        mid = s.top_bar_height // 2
        words = self._text(f'words {s.word_count}', self.small_font, self.hint_color)
        wpm = self._text(f'wpm {s.wpm()}', self.small_font, self.hint_color)
        self.screen.blit(words, words.get_rect(midleft=(20, mid)))
        self.screen.blit(wpm, wpm.get_rect(midright=(self.screen.get_width() - 20, mid)))

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
