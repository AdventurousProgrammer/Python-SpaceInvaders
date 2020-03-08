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
        
    def update_dump(self,bullet,dump):
        last_bullet = self.bullets[len(self.bullets) - 1]                
        bullet_description_x = 'Bullet X Location: ' + str(last_bullet.x)
        bullet_description_y = 'Bullet Y Location: ' + str(last_bullet.y)                
        dump.append(bullet_description_x)
        dump.append(bullet_description_y) 
            
    def shoot(self,game,old_frame,current_frame,initialize,debugging_dump):#any debugging dump can be passed in
        '''
        @FUTURE_NOTICE: really should try to create own test suite, to isolate these problems, or own test functions
        overloading original functions, do not know if that is a good idea
        '''
        #decide how many bullets can be fired based on how many bullets are in list and capacity
        num_bullets_to_add = self.num_bullets - len(self.bullets)
        small_missile = pygame.image.load('small_missile.png')
        ship_center_x = self.x + 0.5*self.width - 12
        ship_center_y = self.y
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
            #print('CAN ADD BULLET')
            if self.weapon == 'REGULAR SHOOTING':
                #print('previous spacebar: ' + str(game.prev_spacebar))
                #print('current spacebar: ' + str(game.current_spacebar))
                if game.current_spacebar and not game.prev_spacebar:
                #    print(datetime.datetime.now())
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,small_missile,5,self.dir)
                    self.bullets.append(bullet)
                    self.update_dump(bullet,debugging_dump)
                #    print('Inside Player Shoot Method: Executing Normal Shooting' )
            
            elif self.weapon == 'RAPID FIRE':
                if game.current_spacebar and current_frame - old_frame > 10:
                    #print('Inside Player Shoot Method: Executing Rapid Fire Shooting')
                    old_frame = current_frame
                    bullet = Player_Projectile(ship_center_x,ship_center_y,12,7,small_missile,5,self.dir)
                    self.bullets.append(bullet)
                    self.update_dump(bullet,debugging_dump)
                    
            elif self.weapon == 'MULTI SHOOTING':
                #press and release spacebar for each 5 missile or 3 missile shot
                cur_i = 0
                offset = 10 #pixel offset from center
                if num_bullets_to_add >= 3 and num_bullets_to_add < 5:
                    max_i = 1
                elif num_bullets_to_add >= 5:
                    max_i = 2
                bullet_position_x = 0
                if game.current_spacebar and not game.prev_spacebar:
                    while cur_i <= max_i:
                        if cur_i == 0:
                            bullet_position_x = ship_center_x
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,small_missile,5,self.dir)
                            self.bullets.append(bullet)
                            self.update_dump(bullet,debugging_dump)
                            cur_i += 1
                        else:
                            #adding right from center bullet
                            bullet_position_x = ship_center_x + cur_i*offset
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,small_missile,10,self.dir)
                            #print('Bullet Position x = ' + str(bullet_position_x))
                            self.bullets.append(bullet)
                            self.update_dump(bullet,debugging_dump)
                            bullet_position_x = ship_center_x + cur_i*offset*-1 # for left bullet
                            bullet = Player_Projectile(bullet_position_x,ship_center_y,12,7,small_missile,10,self.dir)
                            self.update_dump(bullet,debugging_dump)
                            #print('Bullet Position x = ' + str(bullet_position_x))
                            self.bullets.append(bullet)
                            cur_i += 1
        
                
        return old_frame       
               # print('Bullet Time Difference: ' + str(delta.total_seconds()*1000))
               
               
    #index = len(debugging_dump)    
                

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
                  