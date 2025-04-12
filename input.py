import pygame 
import sys 
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
        self.CREATEWORD = pygame.USEREVENT +1
        pygame.time.set_timer(self.CREATEWORD,100)  


    def _update_text(self):
        self.text_gen.update()
        self.text_gen.draw(self.screen)
        # print()
        # self._reaching_right()
        
    def _reaching_right(self):
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


    def _gen_ran_word(self):
        filepath = 'database.txt'
        with open(filepath) as fp:
            self.wordlist = [word.strip() for word in fp.readlines()]
        ran_word = random.choice(self.wordlist)
        self.word = ran_word
        self._create_word(ran_word)

    def _key_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if self.settings.game_active:
                if event.type == self.CREATEWORD:
                    self._gen_ran_word()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_input.clear
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.user_input.append(' ')
                if event.key == pygame.K_RETURN:
                    
                    ans = ''.join(self.user_input)
                    ans = ans.strip()
                    if ans == 'start':
                        self.settings.game_active = True
                        self.settings.initialize_stats()
                    if ans == 'settings':
                        self.settings.go_settings = True 
                    if ans.startswith("word"):
                        print('Yes')
                        parts = ans.split()
                        if len(parts) >= 3 and parts[2].isdigit():
                            self.settings.word_speed = int(parts[2])
                            

                    if ans.startswith("max"):
                        print('Yes')
                        parts = ans.split()
                        if len(parts) >= 3 and parts[2].isdigit():
                            self.settings.max_health = int(parts[2])
                                

                    for word_sprite in self.text_gen.copy():
                        if word_sprite.word== ans:
                            self.text_gen.remove(word_sprite)
                            ans = []
                            self.settings.word_count += 1 
                    self.user_input.clear()

                else:
                    self.user_input.append(event.unicode)

        return self.user_input
    


