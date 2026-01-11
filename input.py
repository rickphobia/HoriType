import pygame 
import os  
from text_gen import Gen_Ran_Word
import random 
from prep_word import PrepMsg
class Input:
    def __init__(self,tg,ui):
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tg.settings
        self.keys = pygame.key.get_pressed()
        self.text_gen = pygame.sprite.Group()
        self.user_input = ui
        self.prep_word = PrepMsg(tg)
        self.invincible_se = self._load_sound('invincible')
        self.reverse_se = self._load_sound('reverse')
        self.freeze_se = self._load_sound('freeze')
        self.clear_se = self._load_sound('clear')
        self.timeslow_se = self._load_sound('timeslow')
        self.CREATEWORD = pygame.USEREVENT +1
        self.CREATEPOWERSUP = pygame.USEREVENT +2 
        pygame.time.set_timer(self.CREATEWORD,100)  
        pygame.time.set_timer(self.CREATEPOWERSUP, 2000)

        # self.reaching_right = True

    def _load_sound(self, name):
        # 1. Try Web (OGG) - Pygbag creates this
        try:
            return pygame.mixer.Sound(f'images/{name}-pygbag.ogg')
        except:
            pass 
        
        # 2. Try Laptop (MP3) - You have this
        try:
            return pygame.mixer.Sound(f'images/{name}.mp3')
        except:
            print(f"Sound Error: Could not load {name}")
            return None
        
    def _update_text(self):
        if self.settings.gen_move_text:
            self.text_gen.update()
        self.text_gen.draw(self.screen)

    def _reaching_right(self):
            for word in self.text_gen.copy():
                if word.rect.right >= self.screen_rect.right:
                    self.text_gen.remove(word)
                    if self.settings.reaching_right:
                        self.settings.health_remain -= 1 

                if self.settings.health_remain == 0:
                    self.settings.game_active = False 
                    for word in self.text_gen.copy():
                        self.text_gen.remove(word)
        
    def _create_word(self,ranword):
        words = Gen_Ran_Word(self,ranword)
        if self.settings.gen_move_text:
            self.text_gen.add(words) 

    def _create_powers_up (self,ran_powersup,power_color):
        powersup = Gen_Ran_Word(self,ran_powersup,color=power_color)
        self.text_gen.add(powersup)

    def _gen_ran_word(self):
        filepath ='database.txt'
        try:
            with open(filepath,'r') as fp:
                self.wordlist = [word.strip() for word in fp.readlines()]
            ran_word = random.choice(self.wordlist)
            self.word = ran_word
            self._create_word(ran_word)     
        except FileNotFoundError:
            print("Error, database.txt nof found ")
            self._create_word("ERRROR")

    def _gen_ran_powersup(self):
        self.powers_dict = {
            'clear' : (255,215,0),
            'freeze': (147,249,255),
            'reverse' : (0,255,0),
            'invincible': (200,65,45), 
            'timeslow' : (64,64,64),
        }   
        ran_powersup = random.choice(list(self.powers_dict.items()))
        power = ran_powersup[0]
        color = ran_powersup[-1]
        self._create_powers_up(power,color)

    def _key_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.settings.game_active = False 
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
        if event.key == pygame.K_BACKSPACE:
            self.user_input.clear()
        if event.key == pygame.K_ESCAPE:
            self.settings.game_active = False 
        if event.key == pygame.K_SPACE:
            self.user_input.append(' ')
        if event.key == pygame.K_RETURN:
            self._process_input()

        else: 
            self.user_input.append(event.unicode)

    # can refactor 
    def _getting_powersup(self,word_sprite):
        if word_sprite.word == 'invincible':
            self.settings.invincible = True 

        if word_sprite.word == 'freeze':
            self.settings.freeze = True 

        if word_sprite.word == 'clear':
            self.settings.clear = True 

        if word_sprite.word == 'timeslow':
            self.settings.timeslow= True 

        if word_sprite.word == 'reverse':
            self.settings.reverse = True 

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

    def _using_powers_up(self,ans):
        #used chatgpt to initialize ideas as well, the rest did i with my own 
        self._activate_clear_powersup(ans)
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

        

        
    def _process_input(self):
        ans = ''.join(self.user_input).strip()
        self._using_powers_up(ans)
        if ans == 'start':
            self.settings.game_active = True
            self.settings.initialize_stats()

        if ans == 'settings':
            self.settings.go_settings = True 

        if ans.startswith("word"):
            self._handle_word_speed_settings(ans)

        if ans.startswith("max"):
            self._handle_max_health_settings(ans)

        for word_sprite in self.text_gen.copy():
            if word_sprite.word == ans:
                self._getting_powersup(word_sprite)
                self.text_gen.remove(word_sprite)
                ans = []
                self.settings.word_count += 1 
        self.user_input.clear()

        return ans 
 



    def _handle_word_speed_settings(self,ans):
            parts = ans.split()
            if len(parts) >= 3 and parts[2].isdigit():
                self.settings.word_speed_const = int(parts[2])
    
    def _handle_max_health_settings(self,ans):
            parts = ans.split()
            if len(parts) >= 3 and parts[2].isdigit():
                self.settings.max_health = int(parts[2])
