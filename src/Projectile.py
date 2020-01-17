import pygame

class Projectile(object):
    bullet_types = ['6','5','7','4','8']
    
    def __init__(self,x,y,width,height,image,vel,dir):
        self.x = x 
        self.y = y
        self.x_vel = 3
        self.y_vel = 3
        self.width = width
        self.height = height
        self.image = image
        self.vel = vel
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.x_dir = 0
        self.y_dir = 0
        
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
        elif self.type == '6':
            self.x_dir = 0
            self.y_dir = 1
            self.x_vel = 0
            self.y_vel = 3     
        elif self.type == '7':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 1
            self.y_vel = 2
        elif self.type == '8':
            self.x_dir = -1
            self.y_dir = 1
            self.x_vel = 2
            self.y_vel = 1
            
    def reverse(self):
        self.x_dir*=-1
        self.y_dir*=-1
            
    def move(self):
        #need to move on to the next level first
        right = self.x_dir == 1 and self.y_dir == 0
        up_right =  self.x_dir == 1 and self.y_dir == -1
        up =   self.y_dir == -1 and self.x_dir == 0
        up_left =  self.x_dir == -1 and self.y_dir == -1
        left = self.x_dir == -1 and self.y_dir == 0
        down_left = self.x_dir == -1 and self.y_dir == 1 
        down = self.y_dir == 1 and self.x_dir == 0
        down_right = self.x_dir == 1 and self.y_dir == 1
#

       # print('Down Right? : ' + str(down_right))
        
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
        
        #self.update_hitbox()
        #if self.missile_type == 'player':
        #    self.hitbox = (self.x + 9,self.y,self.width,self.height + 10)
        #    print('Player Missile hitbox')
        #else:
        #    self.hitbox = (self.x,self.y,self.width,self.height)

class Basic_Enemy_Projectile(Projectile):
    def __init__(self,x,y,width,height,image,vel,dir):
        super().__init__(x,y,width,height,image,vel,dir)
        self.hitbox = (self.x+20,self.y,8,height+20)
        
    def draw(self,win):
        super(Basic_Enemy_Projectile, self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
class Player_Projectile(Projectile):
    #def __init__(self,x,y,width,height,type,image,vel,dir):
    #    super().__init__(x,y,width,height,type,image,vel,dir)
    ##    self.hitbox = (self.x,self.y,self.width,self.height)
    #    self.offset = (9,0,0,10)
    #    self.y_dir = -1
        #self.missile_type = missile_type
        
    def __init__(self,x,y,width,height,image,vel,dir):#not doing anything with dir field
        super().__init__(x,y,width,height,image,vel,dir)#7 arguments
        self.hitbox = (self.x + 9,self.y,self.width,self.height + 10)
    
    def draw(self,win):
        super(Player_Projectile,self).draw(win)
        print(self.hitbox)
        #pygame.draw.rect(win,(255,0,0),self.hitbox+self.offset,2)
        
    def move(self):
        self.y-=self.y_vel
        self.hitbox = (self.x + 9,self.y,self.width,self.height + 10)
        
