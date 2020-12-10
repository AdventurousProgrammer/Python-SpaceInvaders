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
            
    def shoot(self,game,old_frame,current_frame,initialize):#any debugging dump can be passed in
        '''
        @FUTURE_NOTICE: really should try to create own test suite, to isolate these problems, or own test functions
        overloading original functions, do not know if that is a good idea
        '''
     
        num_bullets_to_add = self.num_bullets - len(self.bullets)
        small_missile = 'small_missile.png'
        ship_center_x = self.x + 0.5*self.width - 12
        ship_center_y = self.y
    
        if num_bullets_to_add > 0:
            if self.weapon == 'REGULAR SHOOTING':
                if game.current_spacebar and not game.prev_spacebar:
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                    self.bullets.append(bullet)
            
            elif self.weapon == 'RAPID FIRE':
                if game.current_spacebar and current_frame - old_frame > 10:
                    old_frame = current_frame
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                    self.bullets.append(bullet)
                    
            elif self.weapon == 'MULTI SHOOTING':
                # press and release spacebar for each 5 missile or 3 missile shot
                cur_i = 0
                offset = 10 
                if num_bullets_to_add >= 3 and num_bullets_to_add < 5:
                    max_i = 1
                elif num_bullets_to_add >= 5:
                    max_i = 2
                bullet_position_x = 0
                if game.current_spacebar and not game.prev_spacebar:
                    while cur_i <= max_i:
                        if cur_i == 0:
                            bullet_position_x = ship_center_x
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                            self.bullets.append(bullet)
                            cur_i += 1
                        else:
                            bullet_position_x = ship_center_x + cur_i*offset
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                            self.bullets.append(bullet)
                            bullet_position_x = ship_center_x + cur_i*offset*-1 
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)                   
                            self.bullets.append(bullet)
                            cur_i += 1
                 
        return old_frame
                  