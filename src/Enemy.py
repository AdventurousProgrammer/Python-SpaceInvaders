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
        self.move_next_level = False
    
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
                self.y+=self.y_vel*self.y_dir
            else:
                self.y_dir*=-1
                self.x+=self.x_vel*self.x_dir
            
        self.hitbox = (self.x,self.y,self.width,self.height)
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def hit(self,player_ship):
        player_ship.score += self.score
            
class Multiple_Movement_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height)
        self.hitbox = (x,y,width,height)
        self.type = 'Multiple_Movement_Enemy'            