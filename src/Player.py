import pygame

class Player(object):
    
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bullets = list()
        self.score = 0
        self.image = image
        self.dir = 'up'
        self.vel = 5
        self.pts = 0
        self.health = 100
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.bullets = list()
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def hit(self,pts_lost):
        self.health -= pts_lost
        
            