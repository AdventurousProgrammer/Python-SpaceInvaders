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
        #print('Drawing Ship')
        win.blit(self.image,(self.x,self.y))
        #print('Drew Ship')
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #print('Drew Hitbox')

        
    def hit(self,player_ship):
        player_ship.score += self.score
        
class Horizontal_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot)
        self.right_boundary = 680
        self.left_boundary = 20
        self.top_boundary = 20
        self.bottom_boundary = 680
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)
        
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
            
        if Enemy.move_next_level:
            #print('Y Location: ' + str(self.y))
            #print('Moving Second to Next Layer')
            self.y += self.y_vel*self.y_dir
            self.x_dir *= -1
            
        self.x += self.x_vel*self.x_dir
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)

        
class Vertical_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,x_dir,y_dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,x_dir,y_dir,score,shoot)
        self.right_boundary = 680
        self.left_boundary = 20
        self.top_boundary = 20
        self.bottom_boundary = 680
        self.hitbox = (self.x,self.y,self.width,self.height)
        
    def move(self):
        if self.x <= self.left_boundary and self.x_dir == -1:
            self.x_dir*=-1
        elif self.x_dir == 1 and self.x + self.width >= self.right_boundary:
            self.x_dir*=-1 
        if Enemy.move_next_level:
            #print('Y Location: ' + str(self.y))
            #print('Moving Second to Next Layer')
            self.x += self.x_vel*self.x_dir
            self.y_dir *= -1
    
    
        self.y += self.y_vel*self.y_dir
        self.hitbox = (self.x + 1,self.y + 1,self.width - 2,self.height - 2)
        
    def check_out_of_bounds(self):
        if self.y + self.height >= self.bottom_boundary and self.y_dir == 1 and Enemy.move_next_level == False:
            #self.x += self.x_vel
            #self.dir *= -1
            return True
        elif self.y_dir == -1 and self.y <= self.top_boundary and Enemy.move_next_level == False:
            #self.x += self.x_vel
            #self.dir *= -1
            return True
        return False
    