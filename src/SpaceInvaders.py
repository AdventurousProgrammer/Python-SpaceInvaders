import pygame
import random
import csv
from Enemy import *
from Projectile import *
from Player import *

#TODO: check level arrangement again 6, enemies, then 10 enemies
pygame.init()

screen_width = 700
screen_height = 700


j = 0
win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Space Invaders")

bg = pygame.image.load('starter_background.png')
ship = pygame.image.load('player_ship.png')

ship_vel = 5

small_missile = pygame.image.load('small_missile.png')

num_small_enemies = 6

horizontal_enemy = pygame.image.load('enemy_1.png')
horizontal_enemy_width = 32
horizontal_enemy_height = 31

vertical_enemy = pygame.image.load('enemy_2.png')
vertical_enemy_width = 32
vertical_enemy_height = 32

enemy_missile = pygame.image.load('enemy_missile.png')

current_frame = 0
old_frame = 0

num_levels = 10
distance_index = 0
clock = pygame.time.Clock()
#j = 0
class Game():
    enemies = list()#static variable
    font = pygame.font.SysFont('comicsans', 30, True)
    data = ()
    running = True
    level = 1
    row = 1    

    def redraw_game_window(self,player_ship):
        win.blit(bg,(0,0))
        player_ship.draw(win)
        
        for enemy in self.enemies:
            enemy.draw(win)
            #set enemies and their locations get it from a previous commit
            for bullet in enemy.bullets:
                bullet.draw(win)
            
        for bullet in player_ship.bullets:
            bullet.draw(win) 
    
        text = self.font.render('Score: ' + str(player_ship.score),True,(0,255,0))
        health = self.font.render('Health: ' + str(player_ship.health),True,(255,0,0))
        win.blit(text,(0,0))
        win.blit(health,(300,0))
        pygame.draw.rect(win,(255,0,0),(450,0,player_ship.health,15))
        pygame.display.update()
    
    def overlap_check(self,sprite1,sprite2):
        #add grazing damage
        top_in = sprite1.hitbox[1] > sprite2.hitbox[1] and sprite1.hitbox[1] < sprite2.hitbox[1] + sprite2.hitbox[3]
        bottom_in = sprite1.hitbox[1] + sprite1.hitbox[3] > sprite2.hitbox[1] and sprite1.hitbox[1] + sprite1.hitbox[3] < sprite2.hitbox[1] + sprite2.hitbox[3]
        left_in = sprite1.hitbox[0] > sprite2.hitbox[0] and sprite1.hitbox[0] < sprite2.hitbox[0] + sprite2.hitbox[2]
        right_in = sprite1.hitbox[0] + sprite1.hitbox[2] > sprite2.hitbox[0] and sprite1.hitbox[0] + sprite1.hitbox[2] < sprite2.hitbox[0] + sprite2.hitbox[2]
    
        collision = (bottom_in and right_in) or (left_in and bottom_in) or (top_in and right_in) or (top_in and left_in)    
        return collision
    
    def init(self):
        level_layout = open('levels.csv')
        file_reader = csv.reader(level_layout)
        self.data = list(file_reader)
        print('Data File Set')
            
    def set_level(self):#works
        #if there are more than 5 enemies then just set as 5
        enemy_list = []
        h = 'horizontal_enemy'
        left_x_boundary = 50
        right_x_boundary = screen_width - 50
        top_y_boundary = 50
        bottom_y_boundary = screen_height - 30
        margin = 20
        n = 0
        x_sep = 30
        y_sep = 30
        sprite_width = 32     
        sprite_height = 31
        enemy_type = ''
        num_enemy_type = 0
        enemy = Enemy(0,0,32,31,horizontal_enemy,2,2,1,5,random.randint(0,6))
        j = 0
        while(self.row < len(self.data)):
            if int(self.data[self.row][0]) == self.level:
                #need to update code
                num_enemy_type = int(self.data[self.row][2])
                enemy_type = str(self.data[self.row][1])
                self.row+=1
                
                n = int((screen_width - 2*margin + x_sep)/(x_sep + sprite_width))
                print('N: ' + str(n))
                
                while num_enemy_type > 0:
                    if num_enemy_type <n-1:
                        margin = int(screen_width - (num_enemy_type-1)*(x_sep) - (num_enemy_type-1)*(sprite_width))/2
                        num_enemies = num_enemy_type 
                        num_enemy_type = 0
                        
                    else:
                        margin = int(screen_width - (n-2)*(x_sep) - (n-1)*(sprite_width))/2
                        num_enemies = n-1
                        num_enemy_type -= n-1
                            
                    for k in range(0,num_enemies):
                        if enemy_type == 'Horizontal_Enemy':
                            x_loc = margin + (k%n)*(sprite_width + x_sep)
                            y_loc = top_y_boundary + j*(sprite_height + y_sep) + distance_index*(30+sprite_height)
                            enemy = Horizontal_Enemy(x_loc,y_loc,32,31,horizontal_enemy,2,3,1,5,random.randint(0,6))
                        elif enemy_type == 'Vertical_Enemy':
                            x_loc = left_x_boundary + (k%n)*(sprite_width + x_sep)
                            y_loc = margin + (k%n)*(sprite_height + y_sep) + distance_index*(30+sprite_height)
                            enemy = Vertical_Enemy(x_loc,y_loc,32,32,vertical_enemy,3,2,1,5,random.randint(0,6))
                        enemy_list.append(enemy)
                    j+=1 
                                       #if num_enemy_type > 3:
                 #   n = 3
                #else:
                #    n = num_enemy_type
                    
                #if enemy_type == 'Horizontal_Enemy':
                #    if n == 1:
                       #  x_sep = 0.5*screen_width - margin
               #     else:
               #         x_sep = int((screen_width - 2*(margin) - n*(sprite_width))/(n-1))
               # elif enemy_type == 'Vertical_Enemy':
               #     if n == 1:
               #         y_sep = 0.5*screen_height - margin
               #     else:
               #         y_sep = int((screen_height - 2*(margin) - n*(sprite_height))/(n-1))
                
                #j = 0
                #global distance_index
                #for k in range(0,num_enemy_type):
                   #if k%n == 0 and k!=0:
                   #    j+=1
                   
                #distance_index+=1
            else:
                break
        for enemy in enemy_list:
            print('X Location: ' + str(enemy.x) + ' Y Location: ' + str(enemy.y))
        return enemy_list
           
    def game_over_screen(self):
        print('Game Over')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
    def play(self,player_ship):
        old_frame = 0
        current_frame = 0
        
        while self.running:
            clock.tick(30)
            
            current_frame += 1
            
            if len(self.enemies) <= 0:
                self.enemies = self.set_level()
                self.level += 1
                if len(self.enemies) == 0:
                    print('Game Over: All Levels Completed')
                    self.game_over_screen()
                    
            shoot_flag = random.randint(0,9)
            
            if player_ship.health <= 0:
                self.running = False
                break
            
            if Enemy.move_next_level:
                Enemy.move_next_level = False
                    
            for enemy in self.enemies:
                if enemy.check_out_of_bounds():
                    Enemy.move_next_level = True
                    break
            
            
                    
            for enemy in self.enemies:
                enemy.move()
                if self.overlap_check(enemy,player_ship):
                    if current_frame - old_frame > 3:
                        old_frame = current_frame
                        player_ship.hit(5)
                if enemy.shoot == shoot_flag and len(enemy.bullets) < 1:
                    enemy.bullets.append(Basic_Enemy_Projectile(enemy.x + 0.5*enemy.width,enemy.y + enemy.height,40,26,enemy_missile,4,'down'))
        
            for enemy in self.enemies:
                for bullet in enemy.bullets:#block start
                    if bullet.y > screen_height:
                        enemy.bullets.pop(enemy.bullets.index(bullet))
                        continue
                    bullet.y += bullet.vel
                    bullet.hitbox = (bullet.x + 8,bullet.y,8,bullet.height - 10)
            
                    if self.overlap_check(bullet,player_ship):
                        player_ship.hit(5)
                        enemy.bullets.pop(enemy.bullets.index(bullet))
                        continue
                    
                    for p_bullet in player_ship.bullets:
                        if self.overlap_check(p_bullet,bullet):
                            enemy.bullets.pop(enemy.bullets.index(bullet))
                            player_ship.bullets.pop(player_ship.bullets.index(p_bullet))
                    
            for bullet in player_ship.bullets:
                if bullet.y < 0:
                    player_ship.bullets.pop(player_ship.bullets.index(bullet))
                    continue
                bullet.y -= bullet.vel
                bullet.hitbox = (bullet.x + 9,bullet.y + 1,bullet.width - 6,bullet.height + 7)
                
                for enemy in self.enemies:
                    if self.overlap_check(bullet,enemy):
                        enemy.hit(player_ship)
                        self.enemies.pop(self.enemies.index(enemy))
                        player_ship.bullets.pop(player_ship.bullets.index(bullet))
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE] and len(player_ship.bullets) < 5:
                if current_frame - old_frame > 3:
                    old_frame = current_frame
                    player_ship.bullets.append(Player_Projectile(player_ship.x + 0.5*player_ship.width - 12,player_ship.y,12,7,small_missile,3,player_ship.dir))
           #frame_count += 1
            if keys[pygame.K_RIGHT] and player_ship.x + player_ship.width + player_ship.vel <= screen_width:
                player_ship.x += player_ship.vel
            elif keys[pygame.K_LEFT] and player_ship.x - player_ship.vel >= 0:
                player_ship.x -= player_ship.vel
            elif keys[pygame.K_UP] and player_ship.y - player_ship.vel >= 0:
                player_ship.y -= player_ship.vel
            elif keys[pygame.K_DOWN] and player_ship.y + player_ship.height + player_ship.vel <= screen_height:
                player_ship.y += player_ship.vel
                
            player_ship.hitbox = (player_ship.x,player_ship.y,player_ship.width,player_ship.height)
    
            self.redraw_game_window(player_ship)
        self.game_over_screen()

def main():
    game = Game()
    ship_x = 330
    ship_y = 500
    ship_width = 32
    ship_height = 32
    player_ship = Player(ship_x,ship_y,ship_width,ship_height,ship)
    game.init()
    game.play(player_ship)

if __name__ == '__main__':
    main()