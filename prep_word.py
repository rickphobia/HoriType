import pygame 

class PrepMsg:
    def __init__(self,tg):
        self.screen = tg.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = pygame.display.get_surface().get_size()
        self.width_center, self.height_center = self.width/2, self.height/2
        self.font = pygame.font.SysFont(None, 50)
        self.color = ((255,0,0))

    def game_ends(self):
        word = 'Game Ends'
        self._display_msg(word,self.width_center-500,self.height_center -200)

    def show_word_count (self,word_count):
        msg = f"You have killed {word_count} words"
        self._display_msg(msg,self.width_center -500,self.height_center -150)

    def show_wpm(self,word_count,duration):
        duration = duration/6000
        wpm = int(word_count/duration)
        msg = f"Your WPM is {wpm}"
        self._display_msg(msg,self.width_center -500,self.height_center -100)

    def show_start_button(self):
        word = 'START'
        self._display_msg(word,self.width_center -100,self.height_center-50)
        
    def show_settings(self):
        word = 'SETTINGS'
        self._display_msg(word,self.width_center-100,self.height_center)


    def show_word_speed(self,word_speed):
        word = f"Word speed = {word_speed}"
        self._display_msg(word,self.width_center,self.height_center+50)
    
    # def show_word_gen(self):
    #     word = "Words Generated per seconds = "

    def _display_msg(self,msg,pos_x, pos_y):
        self.image = self.font.render(msg,True,self.color)
        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (pos_x, pos_y))