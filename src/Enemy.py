import pygame
import random
from SpaceInvaders import current_frame
from Projectile import *

class Enemy(object):
    move_next_level = False
    
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.dead = False
        self.score = score
        self.shoot_flag = shoot
        self.bullets = list()
        self.right_boundary = screen_width - 20
        self.left_boundary = 20
        self.top_boundary = 20
        self.bottom_boundary = screen_height - 20
        self.move_next_level = False
        self.switch = 1
        self.name = ''
        self.num_bullets = num_bullets
        self.health = health
                                   
    def set_direction(self,dir):
        x_dir = 0 
        y_dir = 0
                            
        if dir == 0:
            x_dir = 1              
        elif dir == 1:
            x_dir = 1
            y_dir = -1
        elif dir == 2:
            y_dir = -1
        elif dir == 3:
            x_dir = -1
            y_dir = -1
        elif dir == 4:
            x_dir = -1
        elif dir == 5:
            x_dir = -1
            y_dir = 1
        elif dir == 6:
            y_dir = 1
        elif dir == 7:
            x_dir = 1
            y_dir = 1
            
        self.x_dir = x_dir
        self.y_dir = y_dir
        
    def right_out_of_bounds(self):
        return self.x + self.width + self.x_vel>= self.right_boundary
    
    def left_out_of_bounds(self):
        return self.x - self.x_vel<= self.left_boundary
    
    def top_out_of_bounds(self):
        return self.y - self.y_vel<= self.top_boundary
    
    def bottom_out_of_bounds(self):
        return self.y + self.height + self.y_vel>= self.bottom_boundary
    
    def check_out_of_bounds(self): 
        #find out direction to move next layer and return that as tuple
        directions = list()
        
        if self.right_out_of_bounds():
            directions.append('left')
        elif self.left_out_of_bounds():
            directions.append('right')
        if self.top_out_of_bounds():
            directions.append('down')
        elif self.bottom_out_of_bounds():
            directions.append('up')
            
        return directions
        
    def move(self):
        #need to move on to the next level first
        will_be_within_left = self.x - self.x_vel >= self.left_boundary
        will_be_within_right = self.x + self.width + self.x_vel <= self.right_boundary
        will_be_within_top = self.y - self.y_vel >= self.top_boundary
        will_be_within_bottom = self.y + self.height + self.y_vel <= self.bottom_boundary
        
        right = will_be_within_right and self.x_dir == 1 and self.y_dir == 0
        up_right = will_be_within_right and will_be_within_top and self.x_dir == 1 and self.y_dir == -1
        up = will_be_within_top and self.y_dir == -1 and self.x_dir == 0
        up_left = will_be_within_left and will_be_within_top and self.x_dir == -1 and self.y_dir == -1
        left = will_be_within_left and self.x_dir == -1 and self.y_dir == 0
        down_left = will_be_within_left and will_be_within_bottom and self.x_dir == -1 and self.y_dir == 1 
        down = will_be_within_bottom and self.y_dir == 1 and self.x_dir == 0
        down_right = will_be_within_right and self.x_dir == 1 and will_be_within_bottom and self.y_dir == 1
#
        if right:
            self.x+=self.x_vel*self.x_dir 
        elif up_right:
            self.x+=self.x_vel*self.x_dir
            self.y+=self.y_vel*self.y_dir
        elif up:
            self.y+=self.y_vel*self.y_dir
        elif up_left:
            self.x+=self.x_vel*self.x_dir
            self.y+=self.y_vel*self.y_dir
        elif left:
            self.x+=self.x_vel*self.x_dir
        elif down_left:
            self.x+=self.x_vel*self.x_dir
            self.y+=self.y_vel*self.y_dir
        elif down:
            self.y+=self.y_vel*self.y_dir
        elif down_right:
            self.x+=self.x_vel*self.x_dir
            self.y+=self.y_vel*self.y_dir
            
        self.hitbox = (self.x,self.y,self.width,self.height)
    
    def descend_next_level(self,directions):
        for direction in directions:
            if direction == 'right' or direction == 'left':
                self.x_dir*=-1
                if self.top_out_of_bounds() or self.bottom_out_of_bounds():
                    self.switch *= -1
                self.y+=self.y_vel*self.switch
            else:
                self.y_dir*=-1
                if self.right_out_of_bounds() or self.left_out_of_bounds():
                    self.switch *= -1
                self.x+=self.x_vel*self.switch
            
        self.hitbox = (self.x,self.y,self.width,self.height)
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def hit(self,player_ship):
        self.health-=1
        print('Enemy Health: ' + str(self.health))
        if self.health <= 0:
            player_ship.score += self.score
            return True
        return False
    
    def _set_bullet_position(self):
        current_bullet_position_x = self.x + 0.5*self.width - 30
        current_bullet_position_y = self.y + self.height - 25
        
        return (current_bullet_position_x,current_bullet_position_y)
    
    def shoot(self,fire):
        current_bullet_position_x,current_bullet_position_y = self._set_bullet_position()
        num_active_bullets = len(self.bullets)
        bullets_left = self.num_bullets - num_active_bullets
                
        if fire == True:
            add_bullet = True
            default_position = '6'
            if self.type == 'Boss':
                damage = 10
            else:
                damage = 5
                
            if self.num_bullets == 1:
                # will eventually need to change instantiation based on bullet type, will refactor that later
                
                # now that the Projectile constructor has changed a bit, image_name is now a field, coming right after type, which 
                # which needs to get set alongside the type 
                if self.type == 'Boss':
                    image = 'boss_6_position.png'
                else:
                    image = 'enemy_6_position.png'
                     # need to change the damage
                     # need to change the image
                bullet = Basic_Enemy_Projectile(current_bullet_position_x,current_bullet_position_y,40,26,default_position,image,4,'down',damage)
                self.bullets.append(bullet)
                bullet.number = len(self.bullets)
               
            else:
                bullet_type = '6'
                bullet_list_length = len(Projectile.bullet_types)
                bullets_left = self.num_bullets - len(self.bullets)
                print('Num Bullets Left: ' + str(bullets_left))
                bullet_number = 0
                horizontal_gap = 20
                while bullets_left > 0:           
                    if self.type == 'Boss':
                        image = 'boss_6_position.png'
                    else:
                        image = 'enemy_6_position.png'
                    x = current_bullet_position_x + bullet_number*horizontal_gap - 50
                    bullet_number+=1
                    bullet = Basic_Enemy_Projectile(x,current_bullet_position_y,40,26,bullet_type,image,4,'down',damage)
                    self.bullets.append(bullet)
                    bullets_left-=1
                  
class Multiple_Movement_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x,y,width,height)
        self.type = 'Multiple_Movement_Enemy'
              
class Erratic_Movement_Enemy(Enemy):             
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x+10,y,width,height)
        self.type = 'Erratic_Movement_Enemy' 
          
    def move(self,current_movement,old_movement):
        x = False
        if current_movement - old_movement >= 50:
            direction = random.randint(0,7)
            super().set_direction(direction)
            #print(self.name + ' Direction: ' + str(direction))
            x = True
        super().move()
        return x
    
class Deflector_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x,y,width,height)
        self.type = 'Deflector_Enemy' 
        
    def hit(self,player_ship,bullet,current_frame):
        '''
        Enemy is hit, now there needs to be a delay, of a few (< 9) frames, and the bullet can move again later
        '''
        destroyed = super().hit(player_ship) # going to change next iteration
        if destroyed == False:
            bullet.reverse(current_frame)
            print()
            print('Bullet Deflected')
        return destroyed          
    
class Boss(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x+3,y,width-5,height-23)
        self.previous_health = health
        self.current_health = health
        self.wave = 1
        self.current_movement = 0
        self.previous_movement = 0
        self.type = 'Boss'
        self.score = 10
        
    def set_wave(self):
        three_quarter_health = 0.75 * self.health
        half_health = 0.5 * self.health
        quarter_health = 0.25 * self.health
        
        if self.previous_health > three_quarter_health and self.current_health <= three_quarter_health:
            self.wave = 2
            # can shoot multi directional bullets
            
        elif self.previous_health > half_health and self.current_health <= half_health:
            self.x_vel = 5
            self.wave = 3
            
        elif self.previous_health > quarter_health and self.current_health <= quarter_health:
            # move like a random movement self 
            self.wave = 4
            
    def move(self):
        if self.wave == 1 or self.wave == 2 or self.wave == 3:
            self.set_direction(0)
            Multiple_Movement_Enemy.move()
            
        elif self.wave == 4:
            Erratic_Movement_Enemy.move()
            
        self.hitbox = (self.x,self.y,self.width,self.height)
             
    def _set_bullet_position(self):
        current_bullet_position_x = self.x + 0.5*self.width - 30
        current_bullet_position_y = self.y + self.height - 25
        return (current_bullet_position_x,current_bullet_position_y)
    
    def shoot(self,fire):
        super().shoot(fire)
    
    # also returns if boss is destroyed    
    def hit(self,player_ship,bullet):
        self.previous_health = self.current_health
        self.current_health -= bullet.damage
        
        if self.current_health <= 0:
            player_ship.score += self.score
        return self.current_health <= 0
        # set previous health to current_health
       # need to take bullet in, update boss health with bullet damage
            
        
        
        
        