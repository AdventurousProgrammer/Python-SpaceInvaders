import pygame

class Projectile(object):
    def __init__(self,x,y,width,height,image,vel,dir):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.vel = vel
        self.hitbox = (self.x,self.y,self.width,self.height)

    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

class Basic_Enemy_Projectile(Projectile):
    def __init__(self,x,y,width,height,image,vel,dir):
        super().__init__(x,y,width,height,image,vel,dir)
        self.hitbox = (self.x + 8,self.y,8,height - 10)
        
    def draw(self,win):
        super(Basic_Enemy_Projectile, self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        

class Player_Projectile(Projectile):
    def __init__(self,x,y,width,height,image,vel,dir):
        super().__init__(x,y,width,height,image,vel,dir)
        self.hitbox = (self.x + 9,self.y,self.width,self.height + 10)
    
    def draw(self,win):
        super(Player_Projectile,self).draw(win)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)