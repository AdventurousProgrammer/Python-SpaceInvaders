import pygame
import datetime
from src.Projectile import *
from pygame import mixer

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
        self.x_speed = 0
        self.y_speed = 0

    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def hit(self,pts_lost):
        self.health -= pts_lost

    def set_x_speed(self,speed):
        self.x_speed = speed

    def set_y_speed(self,speed):
        self.y_speed = speed

    def shoot(self,game,old_frame,current_frame,initialize):
        num_bullets_to_add = self.num_bullets - len(self.bullets)
        small_missile = 'small_missile.png'
        ship_center_x = self.x + 0.5*self.width - 12
        ship_center_y = self.y
        bullet_sound = mixer.Sound('laser.wav')

        if num_bullets_to_add > 0:
            if self.weapon == 'REGULAR SHOOTING':
                if game.current_spacebar and not game.prev_spacebar:
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                    bullet_sound.play()
                    self.bullets.append(bullet)
            
            elif self.weapon == 'RAPID FIRE':
                if game.current_spacebar and current_frame - old_frame > 10:
                    old_frame = current_frame
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                    bullet_sound.play()
                    self.bullets.append(bullet)
                    
            elif self.weapon == 'MULTI SHOOTING':
                # press and release spacebar for each 5 missile or 3 missile shot
                cur_i = 0
                offset = 10 
                if num_bullets_to_add >= 3 and num_bullets_to_add < 5:
                    max_i = 1
                elif num_bullets_to_add >= 5:
                    max_i = 2
                if game.current_spacebar and not game.prev_spacebar:
                    while cur_i <= max_i:
                        if cur_i == 0:
                            bullet_position_x = ship_center_x
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                            bullet_sound.play()
                            self.bullets.append(bullet)
                            cur_i += 1
                        else:
                            bullet_position_x = ship_center_x + cur_i*offset
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                            bullet_sound.play()
                            self.bullets.append(bullet)
                            bullet_position_x = ship_center_x + cur_i*offset*-1 
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,'player',small_missile,5,self.dir,1)
                            bullet_sound.play()
                            self.bullets.append(bullet)
                            cur_i += 1
                 
        return old_frame
                  