import pygame

class Enemy(object):
    move_next_level = False
    
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot):
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
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def hit(self,player_ship):
        player_ship.score += self.score
        
class Horizontal_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot,screen_width,screen_height):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot)
        self.right_boundary = screen_width - 20
        self.left_boundary = 20
        self.top_boundary = 20
        self.bottom_boundary = (screen_height/2) - 20
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
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot)
        self.right_boundary = screen_width - 20
        self.left_boundary = 20
        self.top_boundary = (screen_height/2) + 20
        self.bottom_boundary = screen_height - 20
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
    