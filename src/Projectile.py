import pygame

class Projectile(object):
    bullet_types = ['6','5','7','4','8']
    images = ['']
    def __init__(self,x,y,width,height,type,image,vel,dir,damage):
        self.x = x 
        self.y = y
        self.x_vel = 5
        self.y_vel = 7
        self.image = pygame.image.load(image)
        self.vel = vel
        self.width = self.image.get_width()
        self.height = height
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.x_dir = 0
        self.y_dir = 0
        self.type = type
        self.dead = False
        self.damage = damage
        self.reversed = False
        
        if self.type != 'player':
            self.set_direction(image)
            
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

    def set_direction(self,image_name):
        if self.type == '4':
            self.x_dir = 1
            self.y_dir = 1
            self.x_vel = 2
            self.y_vel = 3
            missile = image_name
            self.image = pygame.image.load(missile)      
            self.y_vel = 1      
        elif self.type == '5':
            self.x_dir = 1
            self.y_dir = 1
            self.x_vel = 1
            self.y_vel = 2     
            missile = image_name
            self.image = pygame.image.load(missile)    
        elif self.type == '6':
            self.x_dir = 0
            self.y_dir = 1
            self.x_vel = 0
            self.y_vel = 3
            missile = image_name
            self.image = pygame.image.load(missile)    
        elif self.type == '7':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 1
            self.y_vel = 2
            missile = image_name
            self.image = pygame.image.load(missile) 
        elif self.type == '8':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 2
            self.y_vel = 1
            missile = image_name
            self.image = pygame.image.load(missile) 
            
    def reverse(self,current_frame):
        self.x_dir*=-1
        self.y_dir*=-1
        self.reversed = True
        self.last_stopped = current_frame
            
    def move(self):
        right = self.x_dir == 1 and self.y_dir == 0
        up_right =  self.x_dir == 1 and self.y_dir == -1
        up =   self.y_dir == -1 and self.x_dir == 0
        up_left =  self.x_dir == -1 and self.y_dir == -1
        left = self.x_dir == -1 and self.y_dir == 0
        down_left = self.x_dir == -1 and self.y_dir == 1 
        down = self.y_dir == 1 and self.x_dir == 0
        down_right = self.x_dir == 1 and self.y_dir == 1

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
        
class Basic_Enemy_Projectile(Projectile):
    def __init__(self,x,y,width,height,type,image,vel,dir,damage):
        super().__init__(x,y,width,height,type,image,vel,dir,damage)
        self.hitbox = (self.x+51,self.y+8,self.width-99,self.height-7)
        self.number = -1

    def draw(self,win):
        super(Basic_Enemy_Projectile, self).draw(win)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def move(self):
        super().move()
        self.hitbox = (self.x+51,self.y+8,self.width-99,self.height-7)
        #self.hitbox = (self.x + 28,self.y + 25,7,self.height - 10)
        
class Player_Projectile(Projectile):
    def __init__(self,x,y,width,height,type,image,vel,dir,damage):
        super().__init__(x,y,width,height,type,image,vel,dir,damage)
        self.y_dir = -1
        self.reversed = False
        self.hitbox = (self.x + 9,self.y, self.width - 20, self.height + 10)
    
    def draw(self,win):
        super(Player_Projectile,self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self,current_frame):
        if self.reversed == True:
            if current_frame - self.last_stopped > 0:
                self.reversed = False
                super().move()
                self.hitbox = (self.x + 9,self.y,self.width - 20,self.height + 10)
        else:
            super().move()
            self.hitbox = (self.x + 9,self.y,self.width - 20,self.height + 10)