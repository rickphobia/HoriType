import pygame
import random
import time
from text_gen import Gen_Ran_Word
from prep_word import PrepMsg

# words the game treats as commands or power ups, so they never show up as normal words
RESERVED_WORDS = {'start', 'super', 'settings', 'menu', 'back', 'clear', 'freeze', 'reverse', 'invincible', 'timeslow'}

# rows on the settings screen, in the order they are shown
SETTING_ROWS = ['speed', 'health', 'rate']

class Input:
    def __init__(self,tg,ui):
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tg.settings
        self.text_gen = pygame.sprite.Group()
        self.user_input = ui
        self.prep_word = PrepMsg(tg)
        self.word_font = pygame.font.Font('images/font.ttf', self.settings.word_font_size)
        self.invincible_se = self._load_sound('invincible')
        self.reverse_se = self._load_sound('reverse')
        self.freeze_se = self._load_sound('freeze')
        self.clear_se = self._load_sound('clear')
        self.timeslow_se = self._load_sound('timeslow')
        self.CREATEWORD = pygame.USEREVENT +1
        self.CREATEPOWERSUP = pygame.USEREVENT +2
        pygame.time.set_timer(self.CREATEWORD, self.settings.word_interval)
        pygame.time.set_timer(self.CREATEPOWERSUP, self.settings.powersup_interval)
        self.rng = random.Random()
        self.deck = []
        self.selected = 0
        self.death_x = self.screen_rect.right - self.settings.death_margin
        self._load_database()
        self._make_lanes()

    def _load_sound(self, name):
        # 1. Try Web (OGG) - Pygbag creates this
        try:
            return pygame.mixer.Sound(f'images/{name}-pygbag.ogg')
        except Exception:
            pass

        # 2. Try Laptop (MP3) - You have this
        try:
            return pygame.mixer.Sound(f'images/{name}.mp3')
        except Exception:
            print(f"Sound Error: Could not load {name}")
            return None

    def _make_lanes(self):
        # split the play area into rows one line tall, so two words can never sit on top of each other
        top = self.settings.top_bar_height
        bottom = self.screen_rect.height - self.settings.hud_height
        lane_height = self.word_font.get_linesize()
        lane_count = max(1, (bottom - top) // lane_height)
        offset = top + ((bottom - top) - lane_count * lane_height) // 2
        self.lanes = [offset + i * lane_height for i in range(lane_count)]

    def _update_text(self):
        if self.settings.gen_move_text:
            self.text_gen.update()
        self.text_gen.draw(self.screen)

    def _reaching_right(self):
            for word in self.text_gen.copy():
                if word.rect.right >= self.death_x:
                    self.text_gen.remove(word)
                    if self.settings.reaching_right:
                        self.settings.health_remain -= 1

            if self.settings.game_active and self.settings.health_remain <= 0:
                self.end_game()

    def start_game(self, mode='normal'):
        self.settings.mode = mode
        self.settings.initialize_stats()
        self.settings.state = 'playing'
        self.text_gen.empty()
        self.user_input.clear()
        pygame.time.set_timer(self.CREATEWORD, self.settings.word_interval)
        # reseed from the clock on every start so each game gets a new word order,
        # even on the web build where the default seed can repeat between page loads
        self.rng.seed(time.time_ns() ^ pygame.time.get_ticks())
        self.deck = []

    def end_game(self):
        self.settings.state = 'over'
        self.text_gen.empty()
        # drop whatever was half typed so it doesn't stick to the next command
        self.user_input.clear()

    def open_settings(self):
        self.settings.prev_state = self.settings.state
        self.settings.state = 'settings'

    def close_settings(self):
        self.settings.state = self.settings.prev_state

    def _free_lane(self, width):
        # a lane is free once every word in it has moved far enough right of the spawn point
        gap = 40
        free = [
            lane for lane in range(len(self.lanes))
            if all(word.rect.left >= gap for word in self.text_gen if word.lane == lane)
        ]
        if not free:
            return None
        return self.rng.choice(free)

    def _spawn(self, text, color=(255, 255, 255)):
        # no new words while reverse pushes everything back off the left edge
        if not self.settings.gen_move_text or self.settings.reverse_active:
            return
        lane = self._free_lane(self.word_font.size(text)[0])
        if lane is None:
            return
        self.text_gen.add(Gen_Ran_Word(self, text, lane, self.lanes[lane], color=color))

    def _load_database(self):
        try:
            with open('database.txt', 'r') as fp:
                words = [word.strip().lower() for word in fp.readlines()]
        except FileNotFoundError:
            print("Error: database.txt not found")
            words = ["error"]
        # keep the file order only for de-duplicating; the deck is shuffled before use
        self.wordlist = [w for w in dict.fromkeys(words) if w and w not in RESERVED_WORDS]

    def _next_word(self):
        # deal from a shuffled deck: every word shows up once before any word repeats
        on_screen = {word.word for word in self.text_gen}
        for _ in range(len(self.wordlist)):
            if not self.deck:
                self.deck = self.wordlist[:]
                self.rng.shuffle(self.deck)
            word = self.deck.pop()
            if word not in on_screen:
                return word
        return None

    def _gen_ran_word(self):
        ran_word = self._next_word()
        if ran_word:
            self._spawn(ran_word)

    def _gen_ran_powersup(self):
        power, color = self.rng.choice(list(self.settings.powersup_colors.items()))
        if power not in {word.word for word in self.text_gen}:
            self._spawn(power, color)

    def _key_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if self.settings.game_active:
                self._generate_words_powersup(event)

            if event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)

        return self.user_input

    def _generate_words_powersup(self,event):
        if event.type == self.CREATEWORD:
            self._gen_ran_word()

        if event.type == self.CREATEPOWERSUP:
            self._gen_ran_powersup()



    def _handle_keydown_events(self,event):
        state = self.settings.state
        if event.key == pygame.K_BACKSPACE:
            if self.user_input:
                self.user_input.pop()
        elif event.key == pygame.K_ESCAPE:
            self.user_input.clear()
            if state == 'playing':
                self.end_game()
            elif state == 'settings':
                self.close_settings()
            elif state == 'over':
                self.settings.state = 'menu'
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._process_input()
        elif state == 'settings' and event.key in (pygame.K_UP, pygame.K_DOWN):
            step = -1 if event.key == pygame.K_UP else 1
            self.selected = (self.selected + step) % len(SETTING_ROWS)
        elif state == 'settings' and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            step = -1 if event.key == pygame.K_LEFT else 1
            self._change_setting(SETTING_ROWS[self.selected], step)
        elif event.unicode and event.unicode.isprintable():
            if len(self.user_input) < self.settings.max_input_chars:
                self.user_input.append(event.unicode)

    def _change_setting(self, row, step):
        s = self.settings
        if row == 'speed':
            s.word_speed_const = min(max(s.word_speed_const + step, s.min_word_speed), s.max_word_speed)
        elif row == 'health':
            s.max_health = min(max(s.max_health + step, s.min_health), s.max_health_limit)
        elif row == 'rate':
            rates = list(s.word_rates)
            index = min(max(rates.index(s.word_rate) + step, 0), len(rates) - 1)
            self._set_word_rate(rates[index])

    def _set_word_rate(self, rate):
        if rate in self.settings.word_rates:
            self.settings.word_rate = rate
            self.settings.word_interval = self.settings.word_rates[rate]

    # can refactor
    def _getting_powersup(self,word_sprite):
        if word_sprite.word in self.settings.powersup_colors:
            setattr(self.settings, word_sprite.word, True)

    def _play_powersup_se(self,se):
        if se:
            se.play()
    def _activate_powers_up(self,ans,trigger, se):
        active_attr = f"{trigger}_active"
        start_attr = f"{trigger}_start"
        if getattr(self.settings,trigger) and ans == trigger:
            setattr(self.settings,active_attr, True)
            self._play_powersup_se(se)
            setattr(self.settings,start_attr,pygame.time.get_ticks())

    def _activate_clear_powersup(self,ans):
        if self.settings.clear and ans =='clear':
            self.text_gen.empty()
            self._play_powersup_se(self.clear_se)
            self.settings.clear = False
            return True
        return False

    def _using_powers_up(self,ans):
        #used chatgpt to initialize ideas as well, the rest did i with my own
        used_clear = self._activate_clear_powersup(ans)
        self._activate_powers_up(
            ans = ans,
            trigger = 'invincible',
            se = self.invincible_se,
        )
        self._activate_powers_up(
            ans = ans,
            trigger = 'freeze',
            se = self.freeze_se
        )
        self._activate_powers_up(
            ans = ans,
            trigger = 'timeslow',
            se = self.timeslow_se
        )
        self._activate_powers_up(
            ans = ans,
            trigger = 'reverse',
            se = self.reverse_se
        )
        return used_clear


    def _process_input(self):
        ans = ''.join(self.user_input).strip()
        self.user_input.clear()
        command = ans.lower()
        state = self.settings.state

        if state in ('menu', 'over'):
            if command == 'start':
                self.start_game('normal')
            elif command == 'super':
                self.start_game('super')
            elif command == 'settings':
                self.open_settings()
            elif command == 'menu':
                self.settings.state = 'menu'
            return

        if state == 'settings':
            self._handle_settings_command(command)
            return

        if self._using_powers_up(ans):
            return

        # only kill one word per Enter: the one closest to the red line
        matches = [word for word in self.text_gen if word.word == ans]
        if matches:
            word_sprite = max(matches, key=lambda word: word.rect.right)
            self._getting_powersup(word_sprite)
            self.text_gen.remove(word_sprite)
            self.settings.word_count += 1

    def _handle_settings_command(self, command):
        # typed versions of the arrow keys: 'speed 7', 'max health 5', 'rate fast', 'back'
        parts = command.split()
        if not parts or parts[0] in ('back', 'menu', 'settings'):
            self.close_settings()
            return
        s = self.settings
        value = parts[-1]
        if 'speed' in parts and value.isdigit():
            s.word_speed_const = min(max(int(value), s.min_word_speed), s.max_word_speed)
        elif 'health' in parts and value.isdigit():
            s.max_health = min(max(int(value), s.min_health), s.max_health_limit)
        elif 'rate' in parts:
            self._set_word_rate(value)
