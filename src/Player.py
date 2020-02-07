import pygame
from Projectile import *
import datetime

class Player(object):
    
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bullets = list()
        self.score = 0
        self.image = image
        self.dir = 'up'
        self.vel = 5
        self.pts = 0
        self.health = 100
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.bullets = list()
        self.num_bullets = 50
        self.weapon = 'REGULAR SHOOTING'
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def hit(self,pts_lost):
        self.health -= pts_lost
        
    def shoot(self,game,old_frame,current_frame,initialize):
        #decide how many bullets can be fired based on how many bullets are in list and capacity
        num_bullets_to_add = self.num_bullets - len(self.bullets)
       
        #if initialize:
       #     game.prev_spacebar = False
       # else:
       #     game.prev_spacebar = game.current_spacebar #only read when spacebar is pressed;
            #move prev and current spacebar setting to outside shoot function
            #always call shoot, how to deal with initialization
        #game.prev_spacebar = game.current_spacebar
       
        #if statements on weapon types
        #if normal shooting, pass in code for press and release here, decide how many bullets must be fired
        if num_bullets_to_add > 0:
            print('CAN ADD BULLET')
            if self.weapon == 'REGULAR SHOOTING':
                print('previous spacebar: ' + str(game.prev_spacebar))
                print('current spacebar: ' + str(game.current_spacebar))
                if game.current_spacebar and not game.prev_spacebar:
                    print(datetime.datetime.now())
                    ship_center_x = self.x + 0.5*self.width - 12
                    ship_center_y = self.y
                    small_missile = pygame.image.load('small_missile.png')
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,small_missile,5,self.dir)
                    self.bullets.append(bullet)
                    print('Inside Player Shoot Method: Executing Normal Shooting' )
        #if rapid fire shooting pass in code for using delays here, same code in process_input, currently being used on spacebar
        #no other code should have rapid fire settings
        #Multi shooting
        #decide if three bullets or 5 bullets
        #set shooting pattern, inside or all
            #For each bullet
                #calculate bullet position based on center
                #bullet_position = player_ship.x + 0.5*player_ship.width - 12 + index*offset
                #index = 1 for inner shooting areas, otherwise 2
                #offset just based on guess and check
                #then append to bullet list
                  