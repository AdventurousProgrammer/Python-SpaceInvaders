import pygame
import random
import math
from pygame import mixer
import src.Projectile
from src.Projectile import Basic_Enemy_Projectile

def vertical_distance_delay(pixel_delay,y1,y2):
    dist = math.sqrt((y2 - y1)**2)  
    return dist > pixel_delay  
    
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

        if right:
            self.x += self.x_vel * self.x_dir
        elif up_right:
            self.x += self.x_vel * self.x_dir
            self.y += self.y_vel * self.y_dir
        elif up:
            self.y += self.y_vel * self.y_dir
        elif up_left:
            self.x += self.x_vel * self.x_dir
            self.y += self.y_vel * self.y_dir
        elif left:
            self.x += self.x_vel * self.x_dir
        elif down_left:
            self.x += self.x_vel * self.x_dir
            self.y += self.y_vel * self.y_dir
        elif down:
            self.y += self.y_vel * self.y_dir
        elif down_right:
            self.x += self.x_vel * self.x_dir
            self.y += self.y_vel * self.y_dir
        self.hitbox = (self.x, self.y, self.width, self.height)
    
    def descend_next_level(self,directions):
        for direction in directions:
            if direction == 'right' or direction == 'left':
                self.x_dir *= -1
                if self.top_out_of_bounds() or self.bottom_out_of_bounds():
                    self.switch *= -1
                self.y += self.y_vel * self.switch
            else:
                self.y_dir *= -1
                if self.right_out_of_bounds() or self.left_out_of_bounds():
                    self.switch *= -1
                self.x += self.x_vel * self.switch
        self.hitbox = (self.x, self.y, self.width, self.height)
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def hit(self,player_ship):
        self.health -= 1
        if self.health <= 0:
            player_ship.score += self.score
            return True
        return False
    
    def _set_bullet_position(self):
        current_bullet_position_x = self.x + 0.5*self.width - 30
        current_bullet_position_y = self.y + self.height - 25
        return current_bullet_position_x, current_bullet_position_y
    
    def shoot(self,fire):
        current_bullet_position_x,current_bullet_position_y = self._set_bullet_position()
        num_active_bullets = len(self.bullets)
        bullets_left = self.num_bullets - num_active_bullets
        bullet_sound = mixer.Sound('Entities/Player/sounds/laser.wav')
        if fire == True:
            default_position = '6'
            if self.type == 'Boss':
                damage = 10
            else:
                damage = 5
            if self.num_bullets == 1:
                if self.type == 'Boss':
                    image = 'Entities/Enemy/Boss/boss_6_position.png'
                else:
                    image = 'Entities/Enemy/enemy_6_position.png'
                bullet = Basic_Enemy_Projectile(current_bullet_position_x,current_bullet_position_y,40,26,default_position,image,4,'down',damage)
                self.bullets.append(bullet)
                bullet_sound.play()
                bullet.number = len(self.bullets)
            else:
                if len(self.bullets) > 0:
                    last_bullet = self.bullets[-1]
                    if vertical_distance_delay(30,current_bullet_position_y,last_bullet.y) == False:
                        return
                # multi shot    
                bullet_type = '6'
                bullets_left = self.num_bullets - len(self.bullets)
                bullet_number = 0
                horizontal_gap = 20
                while bullets_left > 0:           
                    if self.type == 'Boss':
                        image = 'Entities/Enemy/Boss/boss_6_position.png'
                    else:
                        image = 'Entities/Enemy/enemy_6_position.png'
                    x = current_bullet_position_x + bullet_number*horizontal_gap - 50
                    bullet_number+=1
                    bullet = Basic_Enemy_Projectile(x,current_bullet_position_y,40,26,bullet_type,image,4,'down',damage)
                    self.bullets.append(bullet)
                    bullet_sound.play()
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
            x = True
        super().move()
        return x
    
class Deflector_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x,y,width,height)
        self.type = 'Deflector_Enemy' 
        
    def hit(self,player_ship,bullet,current_frame):
        destroyed = super().hit(player_ship)
        if destroyed == False:
            bullet.reverse(current_frame)
            print()
            #print('Bullet Deflected')
        return destroyed          
    
class Boss(Enemy):
    #TODO: (Last) finish boss functionality
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health):
        super().__init__(x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height,num_bullets,health)
        self.hitbox = (x+3,y,width-5,height-23)
        self.previous_health = health
        self.current_health = health
        self.wave = 1
        self.current_movement = 0
        self.previous_movement = 0
        self.type = 'Boss'
        self.move_type = 'Horizontal_Enemy'
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
            
    def move(self, current_movement, old_movement):
        if self.wave == 1 or self.wave == 2 or self.wave == 3:
            directions = self.check_out_of_bounds()
            if len(directions) > 0:
                self.descend_next_level(directions)
            super().move()
        elif self.wave == 4:
            directions = self.check_out_of_bounds()
            if len(directions) > 0:
                self.descend_next_level(directions)
            x = False
            if current_movement - old_movement >= 50:
                direction = random.randint(0, 7)
                super().set_direction(direction)
                x = True
            super().move()
            return x

        self.hitbox = (self.x,self.y,self.width,self.height)
             
    def _set_bullet_position(self):
        current_bullet_position_x = self.x + 0.5 * self.width - 30
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