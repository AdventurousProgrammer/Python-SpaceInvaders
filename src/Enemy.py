import pygame

class Enemy(object):
    move_next_level = False
    
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height):
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
        self.shoot = shoot
        self.bullets = list()
        self.right_boundary = screen_width - 20
        self.left_boundary = 20
        self.top_boundary = 20
        self.bottom_boundary = screen_height - 20
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def hit(self,player_ship):
        player_ship.score += self.score
        
class Horizontal_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height)
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)
        self.type = 'Horizontal_Enemy'
        
    def check_out_of_bounds(self):
        if self.x_dir == 1 and self.x + self.width >= self.right_boundary and Enemy.move_next_level == False:
           return True
        elif self.x_dir == -1 and self.x <= self.left_boundary and Enemy.move_next_level == False:
            return True
        else:
            return False
    
    def move(self):
        if self.y_dir == -1 and self.y <= self.top_boundary:
            self.y_dir*=-1
        elif self.y_dir == 1 and self.y + self.height >= self.bottom_boundary:
            self.y_dir*=-1
            
        if Horizontal_Enemy.move_next_level:
            #print('Y Location: ' + str(self.y))
            #print('Moving Second to Next Layer')
            self.y += self.y_vel*self.y_dir
            self.x_dir *= -1
            
        self.x += self.x_vel*self.x_dir
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)

        
class Vertical_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height)
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.type = 'Vertical_Enemy'
        
    def move(self):
        if self.x <= self.left_boundary and self.x_dir == -1:
            self.x_dir*=-1
        elif self.x_dir == 1 and self.x + self.width >= self.right_boundary:
            self.x_dir*=-1 
        if Vertical_Enemy.move_next_level:
            self.x += self.x_vel*self.x_dir
            self.y_dir *= -1
    
    
        self.y += self.y_vel*self.y_dir
        self.hitbox = (self.x + 1,self.y + 1,self.width - 2,self.height - 2)
        
    def check_out_of_bounds(self):
        if self.y + self.height >= self.bottom_boundary and self.y_dir == 1 and Enemy.move_next_level == False:
            return True
        elif self.y_dir == -1 and self.y <= self.top_boundary and Enemy.move_next_level == False:
            return True
        return False
    
class Multiple_Movement_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height)
        self.hitbox = ()
        self.type = 'Multiple_Movement_Enemy'
        
    def move(self):
        will_be_within_left = self.x - self.x_vel >= 20
        will_be_within_right = self.x + self.width + self.x_vel <= screen_width - 20
        will_be_within_top = self.y - self.y_vel >= 20
        will_be_within_bottom = self.y + self.height + self.y_vel <= screen_height
        
        right = will_be_within_right and self.x_dir == 1 
        up_right = will_be_within_right and will_be_within_top and self.x_dir == 1 and self.y_dir == -1
        up = will_be_within_top and self.y_dir == -1
        up_left = will_be_within_left and will_be_within_top and self.x_dir == -1 and self.y_dir == -1
        left = will_be_within_left and self.x_dir == -1
        down_left = will_be_within_left and will_be_within_bottom and self.x_dir == -1 and self.y_dir == 1 
        down = will_be_within_bottom and self.y_dir == 1
        down_right = will_be_within_right and self.x_dir == 1 and will_be_within_bottom and self.y_dir == 1
        
        if right:
            self.x+=self.x_vel 
        elif up_right:
            self.x+=self.x_vel
            self.y-=self.y_vel
        elif up:
            self.y-=self.y_vel
        elif up_left:
            self.x-=self.x_vel
            self.y-=self.y_vel
        elif left:
            self.x-=self.x_vel
        elif down_left:
            self.x-=self.x_vel
            self.y+=self.y_vel
        elif down:
            self.y+=self.y_vel
        elif down_right:
            self.x+=self.x_vel
            self.y+=self.y_vel            