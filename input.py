import pygame 
import sys 
from text_gen import Gen_Ran_Word
import random 
from prep_word import PrepMsg
from time import sleep
class Input:
    def __init__(self,tg,ui):
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tg.settings
        self.keys = pygame.key.get_pressed()
        self.text_gen = pygame.sprite.Group()
        self.user_input = ui
        self.prep_word = PrepMsg(tg)
        self.CREATEWORD = pygame.USEREVENT +1
        self.CREATEPOWERSUP = pygame.USEREVENT +2 
        pygame.time.set_timer(self.CREATEWORD,100)  
        pygame.time.set_timer(self.CREATEPOWERSUP, 2000)

        self.reaching_right = True

    def _update_text(self):
        self.text_gen.update()
        self.text_gen.draw(self.screen)

    def _reaching_right(self):
        while self.reaching_right:
            for word in self.text_gen.copy():
                if word.rect.right >= self.screen_rect.right:
                    self.text_gen.remove(word)
                    self.settings.health_remain -= 1 
                    print('Hit')

                if self.settings.health_remain == 0:
                    self.settings.game_active = False 
                    for word in self.text_gen.copy():
                        self.text_gen.remove(word)
        
    def _create_word(self,ranword):
        words = Gen_Ran_Word(self,ranword)
        self.text_gen.add(words) 

    def _create_powers_up (self,ran_powersup,power_color):
        powersup = Gen_Ran_Word(self,ran_powersup,color=power_color)
        self.text_gen.add(powersup)

    def _gen_ran_word(self):
        filepath = 'E:\\programming\\project\\horitype\\database.txt'
        with open(filepath) as fp:
            self.wordlist = [word.strip() for word in fp.readlines()]
        ran_word = random.choice(self.wordlist)
        self.word = ran_word
        self._create_word(ran_word)

    def _gen_ran_powersup(self):
        self.powers_dict = {
            'clear' : (255,215,0),
            'freeze': (147,249,255),
            'reverse' : (0,255,0),
            'invincible': (200,65,45), 
            'time' : (225,235,237)
        }   
        ran_powersup = random.choice(list(self.powers_dict.items()))
        power = ran_powersup[0]
        color = ran_powersup[-1]
        self._create_powers_up(power,color)

    def _key_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
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
                sys.exit()
        if event.key == pygame.K_SPACE:
                self.user_input.append(' ')
        if event.key == pygame.K_RETURN:
            self._process_input(event)

    def _process_input(self,event):
        ans = ''.join(self.user_input)
        ans = ans.strip()
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
            if ans == word_sprite.word:
                if word_sprite.word == 'invinsible':
                    self.reaching_right = False
                    sleep(3)
                    self.reaching_right = True 

                if word_sprite.word == 'freeze':
                     sleep(3)

                if word_sprite.word == 'clear':
                     word_sprite.clear()
                self.text_gen.remove(word_sprite)
                ans = []
                self.settings.word_count += 1 
                self.user_input.clear()

            else:
                self.user_input.append(event.unicode)



    def _handle_word_speed_settings(self,ans):
            parts = ans.split()
            if len(parts) >= 3 and parts[2].isdigit():
                self.settings.word_speed = int(parts[2])
    
    def _handle_max_health_settings(self,ans):
            parts = ans.split()
            if len(parts) >= 3 and parts[2].isdigit():
                self.settings.max_health = int(parts[2])
