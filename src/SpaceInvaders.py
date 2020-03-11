import pygame
import random
import csv
from Enemy import *
from Projectile import *
from Player import *
import math
import datetime


pygame.init()

screen_width = 700
screen_height = 700

BLACK = (0,0,0)

j = 0
win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Space Invaders")

bg = pygame.image.load('starter_background.png')
ship = pygame.image.load('player_ship.png')

ship_vel = 5

small_missile = pygame.image.load('small_missile.png')

num_small_enemies = 6

multiple_movement_enemy_image = pygame.image.load('enemy_2.png')
enemy_width = 32
enemy_height = 31

enemy_missile = pygame.image.load('enemy_missile.png')

current_frame = 0
old_frame = 0

num_levels = 10
distance_index = 0
clock = pygame.time.Clock()

def draw_debugging_dump_output(debugging_dump):
    index = 0
    for i in range(0,len(debugging_dump) - 1):
        text_x = 100
        text_y = 580           
        bullet_description_x = debugging_dump[i]
        bullet_description_y = debugging_dump[i + 1]
        draw_text(bullet_description_x,20,(255,51,153),text_x + index*150,text_y)
        draw_text(bullet_description_y,20,(255,51,153),text_x + index*150,text_y + 75)
        i += 1
        index += 1
        
def draw_text(text,size,color,x,y):
    font = pygame.font.SysFont('comicsans',size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    win.blit(text_surface,text_rect)


class Game():
    enemies = list()
    font = pygame.font.SysFont('comicsans', 30, True)
    data = ()
    running = True
    level = 1
    row = 1    
    num_level_enemies = 0
    prev = False
    current = False
    prev_spacebar = False
    current_spacebar = True
    count = 0
    
    def _distance_delay(self,pixel_delay,x1,y1,x2,y2): 
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist > pixel_delay  
    
    def process_user_input(self,player_ship,old_frame,current_frame,a,debugging_dump):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] and player_ship.x + player_ship.width + player_ship.vel <= screen_width - 20:
            player_ship.x += player_ship.vel
        elif keys[pygame.K_LEFT] and player_ship.x - player_ship.vel >= 20:
            player_ship.x -= player_ship.vel
        elif keys[pygame.K_DOWN] and player_ship.y + player_ship.height + player_ship.vel <= screen_height - 20:
            player_ship.y += player_ship.vel
        elif keys[pygame.K_UP] and player_ship.y - player_ship.vel >= 500:
            player_ship.y -= player_ship.vel
            
        player_ship.hitbox = (player_ship.x,player_ship.y,player_ship.width,player_ship.height)
        
        self._process_weapons(player_ship)
        
        #if keys[pygame.K_SPACE] and len(player_ship.bullets) < player_ship.num_bullets:
        #    print('INSIDE PROCESS USER INPUT: CREATING BULLET NOW')
        #    initialize = False
        if self.count == 0:
            initialize = True
        else:
            initialize = False
                  
        if initialize:
            self.prev_spacebar = False
        else:
            self.prev_spacebar = self.current_spacebar
                
        keys = pygame.key.get_pressed()
        self.current_spacebar = keys[pygame.K_SPACE]
        old_frame = player_ship.shoot(self,old_frame,current_frame,initialize,debugging_dump)
        initialize = False
        self.count = 1
            #trigger shoot method  
            ### DO NOT REMOVE WILL NEED CODE LATER: if current_frame - old_frame > 5:
               # b = datetime.datetime.now()
            ### DO NOT REMOVE WILL NEED CODE LATER: old_frame = current_frame
               # delta = b - a
               # print('Bullet Time Difference: ' + str(delta.total_seconds()*1000))
               # player_ship.bullets.append(Player_Projectile(player_ship.x + 0.5*player_ship.width - 12,player_ship.y,12,7,small_missile,5,player_ship.dir))
        
        return old_frame
    
    def _process_weapons(self,player_ship):
        
        keys = pygame.key.get_pressed()
    
        self.prev = self.current
        self.current = keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4] or keys[pygame.K_5]
        if self.current and not self.prev:
        #BUTTONS WILL NEVER BE PRESSED AT SAME TIME MOST LIKELY
            orange = (255,165,0)
            size = 20
            x = screen_width/2
            y = 500
            
            if keys[pygame.K_1]:
                player_ship.weapon = 'REGULAR SHOOTING' 
                draw_text('REGULAR SHOOTING',size,orange,x,y)
                #print('Current 1 Key Pressed: ' + str(self.current))
                #print('Previous 1 Key Pressed: ' + str(self.prev))
                print('REGULAR SHOOTING')
            elif keys[pygame.K_2]:
                player_ship.weapon = 'RAPID FIRE'
                draw_text('REGULAR SHOOTING',size,orange,x,y)
                #print('Current 2 Key Pressed: ' + str(self.current))
                #print('Previous 2 Key Pressed: ' + str(self.prev))
                #print('RAPID FIRE')
            elif keys[pygame.K_3]:
                player_ship.weapon = 'MULTI SHOOTING'
                #print('MULTI SHOOTING')
            elif keys[pygame.K_4]:
                player_ship.weapon = 'ROCKET'
                #print('ROCKET')
            elif keys[pygame.K_5]:
                player_ship.weapon = 'LASER'
                #print('LASER')
            
            
    def redraw_game_window(self,player_ship,old,cur,debugging_dump):
        '''
        @
        @debugging_dump : added for debugging purposes, to check if one missile is moving faster than the others
        
        What I need to do is get the position at frame 1, then 30 frames later get y position for all the missiles and display the difference
        keep the difference up for 30 frames, where again the difference is updated and displayed until 30 frames pass
        '''
        win.blit(bg,(0,0))
        draw_debugging_dump_output(debugging_dump)
        player_ship.draw(win)
        
        for enemy in self.enemies:
            if enemy.dead == False:
                enemy.draw(win)
            for bullet in enemy.bullets:
                bullet.draw(win)
        index = 0    
        for bullet in player_ship.bullets:
            text_x = 100
            text_y = 580
            bullet_location_x = 'Bullet X: ' + str(bullet.x) 
            bullet_location_y = ' Bullet Y: ' + str(bullet.y)
            
            if cur - old > 30:
                print('UPDATE FRAME NOW')
                # add flag to update difference, so when flag is set, then display all differences, which is stored in debugging dump at beginning
                print('CUR: ' + str(cur))
                print('OLD: ' + str(old))
                #take difference in position here debugging_dump[i] -== bullet.y
                draw_text(bullet_location_x,20,(255,51,153),text_x + index*150,text_y)
                draw_text(bullet_location_y,20,(255,51,153),text_x + index*150,text_y + 75)
                index += 1
                old = cur
                       
            bullet.draw(win) 
    
        score = 'Score: ' + str(player_ship.score)
        health = 'Health: ' + str(player_ship.health)
        weapon = 'Current Weapon: ' + str(player_ship.weapon)
        draw_text(score,30,(0,255,0),45,0)
        draw_text(health,30,(255,0,0),351,0)
        draw_text(weapon,20,(255,165,0),150,500)
        
        pygame.draw.rect(win,(255,0,0),(450,0,player_ship.health,15))
        pygame.display.update()
    
        return old
    
    def move_enemies_as_unit(self,current,old):
        directions = list()
        move_flag = False
        for enemy in self.enemies:
            if enemy.dead == True:
                continue
            if enemy.type == 'Erratic_Movement_Enemy':
                continue         
            if move_flag == False:
                directions = enemy.check_out_of_bounds()    
            if len(directions) > 0:#not being true, even at edge   
                move_flag = True
            for e in self.enemies:
                if move_flag:
                    e.descend_next_level(directions)
            directions = list()
            enemy.move()
            
    def move_enemies_individually(self,old_movement,current_movement):
        x = False
        for enemy in self.enemies:
            if enemy.dead == True:
                continue
            if enemy.type == 'Vertical_Enemy' or enemy.type == 'Horizontal_Enemy':
                continue
            if enemy.type == 'Erratic_Movement_Enemy':
                directions = enemy.check_out_of_bounds()
                if len(directions) > 0:
                    enemy.descend_next_level(directions)
                x = enemy.move(current_movement,old_movement)
        if x == True:
            old_movement = current_movement
                    
        return old_movement
    
    def enemy_status_updates(self,old_frame,curent_frame,player_ship,shoot_flag,index):
        bullet_list_length = len(Projectile.bullet_types)
        for enemy in self.enemies:
            if self.overlap_check(enemy,player_ship):
                player_ship.hit(5)        
            if enemy.shoot == shoot_flag and len(enemy.bullets) < enemy.num_bullets and enemy.dead == False:
                fire = True
                current_bullet_position_x = enemy.x + 0.5*enemy.width - 30
                current_bullet_position_y = enemy.y + enemy.height - 25

                num_active_bullets = len(enemy.bullets)
                bullets_left = enemy.num_bullets - num_active_bullets
                        
                if fire == True:
                    #need to create bullets of different directions
                    add_bullet = True
                    if enemy.num_bullets == 1:
                        #original x location: enemy.x + 0.5*enemy.width
                        bullet = Basic_Enemy_Projectile(current_bullet_position_x,current_bullet_position_y,40,26,'6',4,'down')
                        enemy.bullets.append(bullet)
                        bullet.number = len(enemy.bullets)
                       
                    else:
                        bullets_left = enemy.num_bullets - len(enemy.bullets)
                        #print('Number of Bullets Left: ' + str(bullets_left))
                        while bullets_left > 0:           
                                if enemy.type == 'Erratic_Multishoot_Enemy':
                                    index = random.randint(0,bullet_list_length - 1)
                                else:
                                    index = bullets_left-1
                                bullet_type = Projectile.bullet_types[index]
                                enemy.bullets.append(Basic_Enemy_Projectile(current_bullet_position_x,current_bullet_position_y,40,26,bullet_type,4,'down'))#7 arguments
                                bullets_left-=1
                            
    def enemy_ship_bullet_updates(self,player_ship,debugging_dump):
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if bullet.y + bullet.height > screen_height or bullet.x < 20 or bullet.x + bullet.width >= screen_width:
                    removal_index = enemy.bullets.index(bullet)
                    enemy.bullets.pop(removal_index)
                    continue
                bullet.move()
            
                if self.overlap_check(bullet,player_ship):
                    player_ship.hit(5)
                    removal_index = enemy.bullets.index(bullet)
                    enemy.bullets.pop(removal_index)
                    continue
                    
                for p_bullet in player_ship.bullets:
                    if self.overlap_check(p_bullet,bullet):
                        removal_index = enemy.bullets.index(bullet)
                        enemy.bullets.pop(removal_index)
                        debugging_dump.pop(2*removal_index)
                        debugging_dump.pop(2*removal_index)
                        
    def player_ship_bullet_updates(self,player_ship,debugging_dump):
        for bullet in player_ship.bullets:
            if bullet.y < 0:
                removal_index = player_ship.bullets.index(bullet)
                player_ship.bullets.pop(removal_index)   
                debugging_dump.pop(2*removal_index)
                debugging_dump.pop(2*removal_index)
                continue
            bullet.move()
                
            for enemy in self.enemies:
                if enemy.dead == True:
                    continue
                overlap = self.overlap_check(bullet,enemy)
                if overlap:#possible issue here
                    if enemy.type == 'Deflector_Enemy':
                        enemy.dead = enemy.hit(player_ship,bullet)
                    else:
                        enemy.dead = enemy.hit(player_ship)
                    if enemy.dead == True:
                        self.num_level_enemies-=1
                    removal_index = player_ship.bullets.index(bullet)
                    player_ship.bullets.pop(removal_index)   
                    debugging_dump.pop(2*removal_index)
                    debugging_dump.pop(2*removal_index)        
    
    def overlap_check(self,sprite1,sprite2):
        top_in = sprite1.hitbox[1] > sprite2.hitbox[1] and sprite1.hitbox[1] < sprite2.hitbox[1] + sprite2.hitbox[3]
        bottom_in = sprite1.hitbox[1] + sprite1.hitbox[3] > sprite2.hitbox[1] and sprite1.hitbox[1] + sprite1.hitbox[3] < sprite2.hitbox[1] + sprite2.hitbox[3]
        left_in = sprite1.hitbox[0] > sprite2.hitbox[0] and sprite1.hitbox[0] < sprite2.hitbox[0] + sprite2.hitbox[2]
        right_in = sprite1.hitbox[0] + sprite1.hitbox[2] > sprite2.hitbox[0] and sprite1.hitbox[0] + sprite1.hitbox[2] < sprite2.hitbox[0] + sprite2.hitbox[2]
    
        collision = (bottom_in and right_in) or (left_in and bottom_in) or (top_in and right_in) or (top_in and left_in)    
        return collision
    
    def update_level(self,player_ship):
        if self.num_level_enemies <= 0:
            self.level_transition(player_ship)
            self.enemies = self.set_level(player_ship)
            self.num_level_enemies = len(self.enemies)
            self.level += 1
            if self.num_level_enemies == 0:
                self.game_over_screen()
                
    def init(self):
        level_layout = open('levels.csv')
        file_reader = csv.reader(level_layout)
        self.data = list(file_reader)
            
    def set_level(self,player_ship):
        enemy_list = []
        left_x_boundary = 50
        top_y_boundary = 50
        margin = 20
        layer = 0
        n = 0
        x_sep = 30
        y_sep = 30
        sprite_width = 32     
        sprite_height = 31
        enemy_type = ''
        num_enemy_type = 0
        enemy = Enemy(0,0,32,31,multiple_movement_enemy_image,2,2,1,1,5,random.randint(0,6),screen_width,screen_height,0,0)
        j = 0
        levels = list()
        for ii in range(0,len(self.data)):
            levels.append(self.data[ii][0])
        
        while(self.row < len(self.data)):
            if int(self.data[self.row][0]) == self.level:
                num_bullets = int(self.data[self.row][3])
                player_ship.num_bullets = num_bullets
                num_enemy_type = int(self.data[self.row][2])
                enemy_type = str(self.data[self.row][1])
                enemy_num_bullets = int(self.data[self.row][4])
                enemy_health = int(self.data[self.row][5])
                self.row+=1
                margin = 20
                x_sep = 30
                n = int((screen_width - 2*margin + x_sep)/(x_sep + sprite_width))
                
                while num_enemy_type > 0:
                    if num_enemy_type <n-1:
                        margin = int(screen_width - (num_enemy_type-1)*(x_sep) - (num_enemy_type-1)*(sprite_width))/2
                        num_enemies = num_enemy_type 
                        num_enemy_type = 0
                        
                    else:
                        margin = int(screen_width - (n-2)*(x_sep) - (n-1)*(sprite_width))/2
                        num_enemies = n-1
                        num_enemy_type -= n-1
                        
                    dir = 0  
                    image = pygame.image.load('enemy_2.png') 
                         
                    for k in range(0,num_enemies):
                        x_loc = margin + (k%n)*(sprite_width + x_sep)
                        y_loc = top_y_boundary + j*(sprite_height + y_sep)
                        width = 32
                        height = 32
                        x_vel = 3
                        y_vel = 1
                        score = 7
                        shoot = random.randint(0,9)
                        
                        if enemy_type == 'Horizontal_Enemy':
                            enemy = Multiple_Movement_Enemy(x_loc,y_loc,width,height,image,x_vel,y_vel,0,0,score,shoot,screen_width,screen_height,enemy_num_bullets,enemy_health)
                            dir = 0
                        elif enemy_type == 'Vertical_Enemy':
                            enemy = Multiple_Movement_Enemy(x_loc,y_loc,width,height,image,x_vel,y_vel,0,0,score,shoot,screen_width,screen_height,enemy_num_bullets,enemy_health)
                            dir = 2
                        elif enemy_type == 'Multiple_Movement_Enemy':
                            enemy = Multiple_Movement_Enemy(x_loc,y_loc,width,height,image,x_vel,y_vel,0,0,score,shoot,screen_width,screen_height,enemy_num_bullets,enemy_health)
                            dir = random.randint(0,7)
                        elif enemy_type == 'Erratic_Movement_Enemy':
                            enemy = Erratic_Movement_Enemy(x_loc,y_loc,width,height,image,x_vel,y_vel,0,0,score,shoot,screen_width,screen_height,enemy_num_bullets,enemy_health)   
                        elif enemy_type == 'Deflector_Enemy':
                            enemy = Deflector_Enemy(x_loc,y_loc,width,height,image,x_vel,y_vel,0,0,score,shoot,screen_width,screen_height,enemy_num_bullets,enemy_health) 
                        enemy.name = 'Enemy: ' + str(k)                        
                        enemy.set_direction(dir)
                        enemy_list.append(enemy)
                        
                    j+=1
                layer = j                      
            else:
                break
        #for enemy in enemy_list:
        #    print('X Direction: ' + str(enemy.x_dir) + ' Y Direction: ' + str(enemy.y_dir))
        return enemy_list
           
    def game_over_screen(self):
        while True:
            draw_text('Game Over!',30,(255,0,0),screen_width/2,screen_height/2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
    def level_transition(self,player_ship):       
         score = 'Score: ' + str(player_ship.score)
         health = 'Health: ' + str(player_ship.health)
         x = 150
         win.fill((0,0,0))
         while x > 0:
             draw_text(score,30,(0,255,0),45,0)
             draw_text(health,30,(255,0,0),351,0)
             pygame.draw.rect(win,(255,0,0),(450,0,player_ship.health,15))
             draw_text('Level ' + str(self.level) + ' is Starting!',30,(255,128,0),screen_width/2,100)
             player_ship.draw(win)
             
             if self.level == 5:
                 draw_text('Number of Bullets has increased to 7!',30,(255,128,0),screen_width/2,130)
             pygame.display.update()
             pygame.time.delay(20)
             x -= 1
      
    def play(self,player_ship):
        old_frame = 0
        current_frame = 0
        
        old_movement = 0
        current_movement = 0
        a = 0
        b = 0
        old = 0
        cur = 0
        index = 0
        a = datetime.datetime.now()
        x = datetime.datetime.now()
        debugging_dump = list()
        initialize = True
        while self.running:
            a = datetime.datetime.now()
            clock.tick(30)
            current_frame += 1
            current_movement += 1
            cur += 1
            
            self.update_level(player_ship)
            shoot_flag = random.randint(0,9)
            
            if player_ship.health <= 0:
                self.running = False
                break
            
            self.move_enemies_as_unit(current_frame,old_frame) 
            old_movement = self.move_enemies_individually(old_movement,current_movement)
            self.enemy_status_updates(old_frame,current_frame,player_ship,shoot_flag,index)
            self.enemy_ship_bullet_updates(player_ship,debugging_dump)
            self.player_ship_bullet_updates(player_ship,debugging_dump)      
            old_frame = self.process_user_input(player_ship,old_frame,current_frame,a,debugging_dump)
            old = self.redraw_game_window(player_ship,old,cur,debugging_dump)
            b = datetime.datetime.now()
            
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