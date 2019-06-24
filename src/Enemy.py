import pygame

class Enemy(object):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir,score,shoot):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.dir = dir
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
    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,dir,score,shoot)
        self.right_boundary = 650
        self.left_boundary = 50
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)

    def move(self):
        if self.x >= self.right_boundary:
            self.y += self.y_vel
            self.dir *= -1
        elif self.dir == -1 and self.x <= 0:
            self.y += self.y_vel
            self.dir *= -1
    
        self.x += self.x_vel*self.dir
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)
        
class Vertical_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,dir,score,shoot)
        self.right_boundary = 650
        self.left_boundary = 50
        self.top_boundary = 50
        self.bottom_boundary = 650
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)
        
    def move(self):
        if self.y >= self.bottom_boundary:
            self.x += self.x_vel
            self.dir *= -1
        elif self.dir == -1 and self.y <= self.top_boundary:
            self.x += self.x_vel
            self.dir *= -1
    
        self.y += self.y_vel*self.dir
        self.hitbox = (self.x + 8,self.y + 19,self.width - 16,11)