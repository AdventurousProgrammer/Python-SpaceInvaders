import pygame
import random

pygame.init()
screen_width = 700
screen_height = 700
ship_x = 330
ship_y = 500
ship_width = 32
ship_height = 32
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("First Pygame Game")
bg = pygame.image.load('starter_background.png')
ship = pygame.image.load('player_ship.png')
print('Ship Loaded')
ship_vel = 5
small_missile = pygame.image.load('small_missile.png')
num_small_enemies = 6
enemy_1 = pygame.image.load('enemy_1.png')
enemy_missile = pygame.image.load('enemy_missile.png')
#win.blit(ship,(ship_x,ship_y))
#pygame.display.flip()

#classes present in program for now it is just the enemies going to do 1 enemy and then analyze design againc
class Player(object):
    # a player needs to be able to draw itself
    # a player needs an action to happen when he gets hit
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
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def hit(self,pts_lost):
        self.health -= pts_lost

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
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
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
    
class Small_Enemy(Enemy):

    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir,score,shoot):
        super().__init__(x, y, width, height, image,x_vel,y_vel,dir,score,shoot)
        self.right_boundary = 650
        self.left_boundary = 50
        self.hitbox = (self.x,self.y,self.width,self.height)

    def move(self):
        
        if self.x >= self.right_boundary:
            self.y += self.y_vel
            self.dir *= -1
        elif self.dir == -1 and self.x <= 0:#going towards left and not just at the starting point
            self.y += self.y_vel
            self.dir *= -1
    
        self.x += self.x_vel*self.dir
        self.hitbox = (self.x,self.y,self.width,self.height)

    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def hit(self,player_ship):
        player_ship.pts += self.score
        print(player_ship.pts)
        
def redraw_game_window():
    win.blit(bg,(0,0))
    player_ship.draw(win)
    for enemy in small_enemies:
        enemy.draw(win)
        for bullet in enemy.bullets:
            bullet.draw(win)
            
    for bullet in player_ship.bullets:
        bullet.draw(win) 
    
    text = font.render('Score: ' + str(player_ship.pts),True,(255,0,0))#render new text to be put onto screen, turn into surface blit onto screen
    health = font.render('Health: ' + str(player_ship.health),True,(0,255,0))
    win.blit(text,(0,0))
    win.blit(health,(300,0))
    pygame.draw.rect(win,(0,255,0),(450,0,player_ship.health,15))
    pygame.display.update()
    
def overlap_check(sprite1,sprite2):
    
    top_in = sprite1.y > sprite2.y and sprite1.y < sprite2.y + sprite2.height
    bottom_in = sprite1.y + sprite1.height > sprite2.y and sprite1.y + sprite1.height < sprite2.y + sprite2.height
    left_in = sprite1.x > sprite2.x and sprite1.x < sprite2.x + sprite2.width
    right_in = sprite1.x + sprite1.width > sprite2.x and sprite1.x + sprite1.width < sprite2.x + sprite2.width
    
    return (bottom_in and right_in) or (left_in and bottom_in) or (top_in and right_in) or (top_in and left_in)

running = True

clock = pygame.time.Clock()

player_ship = Player(ship_x,ship_y,ship_width,ship_height,ship)
small_enemies = list()
font = pygame.font.SysFont('comicsans', 30, True)    
x_separation = 60
y_separation = 50

for i in range(0,num_small_enemies):
    if i < 3:
        y = 50
        small_enemies.append(Small_Enemy(50 + i*x_separation,y,32,31,enemy_1,5,5,1,10,i))
    else:
        y = 100
        small_enemies.append(Small_Enemy(50 + (i-3)*x_separation,y,32,31,enemy_1,5,5,1,10,i))
        
while running:
    clock.tick(30)
    shoot_flag = random.randint(0,9)
    
    if player_ship.health <= 0:
        running = False
        break
    
    #move enemy and create their bullets (probably should be broken up into separate loops, think of time complexity)
    for enemy in small_enemies:
        enemy.move()
        
        if enemy.shoot == shoot_flag and len(enemy.bullets) < 1:
            enemy.bullets.append(Projectile(enemy.x + 0.5*enemy.width,enemy.y + enemy.height,40,26,enemy_missile,3,'down'))
        #x,y,width,height,image,x_vel,y_vel,dir,score,shoot    
        if overlap_check(enemy,player_ship):
            player_ship.hit(10)
    #moving player bullets and check with enemy collision        
    for bullet in player_ship.bullets:
        if bullet.y < 0:
            player_ship.bullets.pop(player_ship.bullets.index(bullet))
        #add collision code as well
        bullet.y -= bullet.vel
        bullet.hitbox = (bullet.x,bullet.y,bullet.width,bullet.height)
        
        for enemy in small_enemies:
            if overlap_check(bullet,enemy):
                enemy.hit(player_ship)
                small_enemies.pop(small_enemies.index(enemy))
                player_ship.bullets.pop(player_ship.bullets.index(bullet))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    #ship movement and keyboard controls
    if keys[pygame.K_SPACE] and len(player_ship.bullets) < 1:
        player_ship.bullets.append(Projectile(player_ship.x + 0.5*player_ship.width - 5,player_ship.y,12,7,small_missile,3,player_ship.dir))

    if keys[pygame.K_RIGHT] and player_ship.x + player_ship.width + player_ship.vel <= screen_width:
        player_ship.x += player_ship.vel
    elif keys[pygame.K_LEFT] and player_ship.x - player_ship.vel >= 0:
        player_ship.x -= player_ship.vel
    elif keys[pygame.K_UP] and player_ship.y - player_ship.vel >= 0:
        player_ship.y -= player_ship.vel
    elif keys[pygame.K_DOWN] and player_ship.y + player_ship.height + player_ship.vel <= screen_height:
        player_ship.y += player_ship.vel
    
    player_ship.hitbox = (player_ship.x,player_ship.y,player_ship.width,player_ship.height)
    
    redraw_game_window()
    
    
    
#use photoshop to get rid of white space onn sprites
      