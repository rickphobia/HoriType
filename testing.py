import pygame
import sys 


pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()
font = pygame.font.SysFont(None, 50)
color = ((255,0,0))
BRO = pygame.USEREVENT+1
pygame.time.set_timer(BRO, 2000)
user_input = []
ans = []
while True:
    for e in pygame.event.get():
        if e.type == BRO:
            screen.fill((0,0,0))
        if e.type == pygame.KEYDOWN:
            
            if e.key == pygame.K_ESCAPE:
                sys.exit()
            if e.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            if e.key == pygame.K_SPACE:
                user_input.append(' ') 
            if e.key == pygame.K_RETURN:
                ans = ''.join(user_input)
                if ans.startswith('lul'):
                    print("Ues")
                
            else: 
                user_input += e.unicode
        
        input_list = ''.join(user_input)
        image = font.render(input_list, True, color )
        pos_x = 500
        pos_y = 650 
        screen.blit(image,(pos_x,pos_y))
    pygame.display.flip()
