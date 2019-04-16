import pygame
import random
import csv
from Enemy import *
from Projectile import *
from Player import *

pygame.init()

screen_width = 700
screen_height = 700


margin = 40

win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Space Invaders")

bg = pygame.image.load('starter_background.png')
ship = pygame.image.load('player_ship.png')

ship_vel = 5

small_missile = pygame.image.load('small_missile.png')

num_small_enemies = 1

enemy_1 = pygame.image.load('enemy_1.png')
enemy_missile = pygame.image.load('enemy_missile.png')

current_frame = 0
old_frame = 0

num_levels = 10

clock = pygame.time.Clock()

levels = list()

class Game():
    enemies = list()#static variable
    font = pygame.font.SysFont('comicsans', 30, True)
    data = ()
    running = True    

    def redraw_game_window(self,player_ship):
        win.blit(bg,(0,0))
        player_ship.draw(win)
        player_ship.hit(10)
        
        for enemy in Game.enemies:
            enemy.draw(win)
            for bullet in enemy.bullets:
                bullet.draw(win)
            
        for bullet in player_ship.bullets:
            bullet.draw(win) 
    
        text = self.font.render('Score: ' + str(player_ship.score),True,(255,0,0))
        health = self.font.render('Health: ' + str(player_ship.health),True,(0,255,0))
        win.blit(text,(0,0))
        win.blit(health,(300,0))
        pygame.draw.rect(win,(0,255,0),(450,0,player_ship.health,15))
        pygame.display.update()
    
    
    def overlap_check(self,sprite1,sprite2):
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
    
    def set_level(self,row,index):
        enemy_list = {}
        print('i = ' + str(index) + ' New Level')
        while(row < len(self.data)):
            if int(self.data[row][0]) == index:
                enemy_list[self.data[row][1]] = int(self.data[row][2])
                row+=1
            else:
                break
        self._set_enemy_locations(enemy_list)
    
        
    def _set_enemy_locations(self,e):
        num_enemies = len(e)
        x_sep = 30
        y_sep = 30
        sprite_width = self.enemies.get(self.enemies.keys[0]).width     #(n-1)*x_sep + n*ship_width = screen_width - margin
    #n*x_sep - x_sep + n*ship_width = screen_width - margin
         #n = int((screen_width - margin)/(x_sep + sprite_width))
    
         #keys = enemies.keys()
    #get enemy
    #figure out x_sep 
         #x_sep = (screen_width - margin - (n/2)*(ship_width)/(n - 1))
    
         #for i in range(0,len(enemies.keys)):
          #   if enemies:
           #  enemy = eval(enemies.get(enemies.keys[i]))
    #create enemy instance
         #if n > num_enemies/2:
          #   n = num_enemies/2
        #place first ship at left boundary
    #the case with varying ships
    
    def game_over_screen(self,player_ship):
        while True:
            loss_text = self.font.render('Too Bad You Lost! Score:' + str(player_ship.pts),True,(255,0,0))
            win.blit(loss_text,(0,0))
            evil = pygame.image.load('evil.png')
            win.blit(evil,(120,120))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i+=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
    
    def play(self,player_ship):
        old_frame = 0
        current_frame = 0
        while Game.running:
            clock.tick(30)
            current_frame += 1
            shoot_flag = random.randint(0,9)
            
            if player_ship.health <= 0:
                running = False
                break
            
            for enemy in self.enemies:
                enemy.move()
                if self.overlap_check(enemy,player_ship):
                    if current_frame - old_frame > 3:
                        old_frame = current_frame
                        player_ship.hit(10)
                if enemy.shoot == shoot_flag and len(enemy.bullets) < 1:
                    enemy.bullets.append(Basic_Enemy_Projectile(enemy.x + 0.5*enemy.width,enemy.y + enemy.height,40,26,enemy_missile,3,'down'))
        
            for enemy in self.enemies:
                for bullet in enemy.bullets:#block start
                    if bullet.y > screen_height:
                        enemy.bullets.pop(enemy.bullets.index(bullet))
                        continue
                    bullet.y += bullet.vel
                    bullet.hitbox = (bullet.x + 8,bullet.y,8,bullet.height - 10)
            
                    if self.overlap_check(bullet,player_ship):
                        player_ship.hit(10)
                        enemy.bullets.pop(enemy.bullets.index(bullet))
                        continue
                    
                    for p_bullet in player_ship.bullets:
                        if Game.overlap_check(p_bullet,bullet):
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
                        enemy.hit()
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
        self.game_over_screen(player_ship)

def main():
    game = Game()
    ship_x = 330
    ship_y = 500
    ship_width = 32
    ship_height = 32
    player_ship = Player(ship_x,ship_y,ship_width,ship_height,ship)
    #game.init()
    game.play(player_ship)

if __name__ == '__main__':
    main()