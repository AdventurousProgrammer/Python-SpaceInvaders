import pygame
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
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        
    def hit(self):
        pass

class Projectile(object):
    def __init__(self,x,y,width,height,image,vel,dir):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.vel = vel
        
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
        
class Enemy(object):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.dir = dir
        self.dead = False
        #self.score = score
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
    
class Small_Enemy(Enemy):
    def __init__(self,x,y,width,height,image,x_vel,y_vel,dir):
        super().__init__(x, y, width, height, image,x_vel,y_vel,dir)
        self.right_boundary = 650
        self.left_boundary = 50
        
    def move(self):
        if self.x >= self.right_boundary:
            self.y += self.y_vel
            self.dir *= -1
        elif self.dir == -1 and self.x <= 0:#going towards left and not just at the starting point
            self.y += self.y_vel
            self.dir *= -1
    
        self.x += self.x_vel*self.dir
    
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
    
    def hit(self,player_ship):
        player_ship.pts += self.score
        
def redraw_game_window():
    win.blit(bg,(0,0))
    player_ship.draw(win)
    for enemy in small_enemies:
        enemy.draw(win)
    for bullet in player_ship.bullets:
        bullet.draw(win) 
        
    pygame.display.update()

running = True

clock = pygame.time.Clock()

player_ship = Player(ship_x,ship_y,ship_width,ship_height,ship)
small_enemies = list()
x_separation = 40
y_separation = 50
for i in range(0,num_small_enemies):
    if i < 3:
        y = 50
        small_enemies.append(Small_Enemy(50 + i*x_separation,y,32,31,enemy_1,5,5,1))
    else:
        y = 100
        small_enemies.append(Small_Enemy(50 + (i-3)*x_separation,y,32,31,enemy_1,5,5,1))
        
while running:
    clock.tick(30)
    
    for enemy in small_enemies:
        enemy.move()
        
    for bullet in player_ship.bullets:
        if bullet.y < 0:
            player_ship.bullets.pop(player_ship.bullets.index(bullet))
        #add collision code as well
        bullet.y -= bullet.vel
        
        for enemy in small_enemies:
            within_x = bullet.x > enemy.x and bullet.x < enemy.x + enemy.width
            within_y = bullet.y < enemy.y + enemy.height and bullet.y > enemy.y
            if within_x and within_y:
                small_enemies.pop(small_enemies.index(enemy))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and len(player_ship.bullets) < 25:
        player_ship.bullets.append(Projectile(player_ship.x + 0.5*player_ship.width - 5,player_ship.y,12,7,small_missile,3,player_ship.dir))
        #create a bullet at the middle of the ship mouth
    if keys[pygame.K_RIGHT] and player_ship.x + player_ship.width + player_ship.vel <= screen_width:
        player_ship.x += player_ship.vel
    elif keys[pygame.K_LEFT] and player_ship.x - player_ship.vel >= 0:
        player_ship.x -= player_ship.vel
    redraw_game_window()
    
    
#use photoshop to get rid of white space onn sprites
      