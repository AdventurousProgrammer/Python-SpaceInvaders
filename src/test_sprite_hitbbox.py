import pygame
import unittest
from Enemy import Vertical_Enemy
import random

class TestSpriteHitboxes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestSpriteHitboxes, cls).setUpClass()
        pygame.init()
        
    def test_vertical_enemy_hitbox(self):
        win = pygame.display.set_mode((700,700))
        vertical_enemy = pygame.image.load('enemy_2.png')
                            #x,  y, width,height,image,         x_vel,y_vel,x_dir,y_dir,score,shoot
        v = Vertical_Enemy(100,100,32,32,vertical_enemy,3,2,1,1,5,random.randint(0,6))
        v.draw(win)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()