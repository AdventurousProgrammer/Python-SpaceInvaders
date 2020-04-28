import pygame

class Projectile(object):
    bullet_types = ['6','5','7','4','8']
    
    def __init__(self,x,y,width,height,type,image,vel,dir):
        self.x = x 
        self.y = y
        self.x_vel = 5
        self.y_vel = 7
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)
        self.vel = vel
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.x_dir = 0
        self.y_dir = 0
        self.type = type
        self.dead = False
        
        if self.type != 'player':
            self.set_direction()
            
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        
    def set_direction(self):
        if self.type == '4':
            self.x_dir = 1
            self.y_dir = 1
            self.x_vel = 2
            self.y_vel = 3
            missile = 'enemy_4_position.png'
            self.image = pygame.image.load(missile)      
            self.y_vel = 1      
        elif self.type == '5':
            self.x_dir = 1
            self.y_dir = 1
            self.x_vel = 1
            self.y_vel = 2     
            missile = 'enemy_5_position.png'
            self.image = pygame.image.load(missile)    
        elif self.type == '6':
            self.x_dir = 0
            self.y_dir = 1
            self.x_vel = 0
            self.y_vel = 3  
            missile = 'enemy_6_position.png'
            self.image = pygame.image.load(missile)    
        elif self.type == '7':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 1
            self.y_vel = 2
            missile = 'enemy_7_position.png'
            self.image = pygame.image.load(missile) 
        elif self.type == '8':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 2
            self.y_vel = 1
            missile = 'enemy_8_position.png'
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
    def __init__(self,x,y,width,height,type,image,vel,dir):
        super().__init__(x,y,width,height,type,image,vel,dir)
        self.hitbox = (self.x + 28,self.y + 25,7,self.height - 10)
        self.number = -1
        
    def draw(self,win):
        super(Basic_Enemy_Projectile, self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def move(self):
        super().move()
        self.hitbox = (self.x + 28,self.y + 25,7,self.height - 10)
        
class Player_Projectile(Projectile):
    def __init__(self,x,y,width,height,type,image,vel,dir):
        super().__init__(x,y,width,height,type,image,vel,dir)
        self.y_dir = -1
        self.reversed = False
        self.hitbox = (self.x + 9,self.y,self.width - 5,self.height + 10)
    
    def draw(self,win):
        super(Player_Projectile,self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    '''
    TODO
    1. Quit overriding the move method in Projectile
    2. Set x and y directions to bullet
    
    IF bullet has been reversed
       IF time difference is great enough
           SET reversal to FALSE, DO NOT set self.last_stopped
               MOVE BULLET AND HIT BOX
        ELSE DO NOT do anything
               
    ELSE (bullet has not been reversed)
    MOVE BULLET AND HITBOX ACCORDINGLY
    '''    
    def move(self,current_frame):
        if self.reversed == True:
            if current_frame - self.last_stopped > 0:
                print('Move Again')
                self.reversed = False
                super().move()
                self.hitbox = (self.x + 9,self.y,self.width - 5,self.height + 10)
        else:
            super().move()
            self.hitbox = (self.x + 9,self.y,self.width - 5,self.height + 10)
            
        
        #self.y-=self.y_vel
        
        