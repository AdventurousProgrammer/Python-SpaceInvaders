import pygame
pygame.init()
screen_width = 700
screen_height = 700
ship_x = 330
ship_y = 500
ship_width = 46
ship_height = 68
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("First Pygame Game")
bg = pygame.image.load('starter_background.png')
ship = pygame.image.load('nightraiderfixed.png')
ship_vel = 5
win.fill((255,255,255))
#win.blit(ship,(ship_x,ship_y))
#pygame.display.flip()

def redraw_game_window():
    win.blit(bg,(0,0)) 
    win.blit(ship,(ship_x,ship_y))
    pygame.display.update()
    
running = True

clock = pygame.time.Clock()

while running:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT] and ship_x + ship_width + ship_vel <= screen_width:
        ship_x += ship_vel
    elif keys[pygame.K_LEFT] and ship_x - ship_vel >= 0:
        ship_x -= ship_vel
    redraw_game_window()
    
    
#use photoshop to get rid of white space onn sprites
      