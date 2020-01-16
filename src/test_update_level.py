import unittest
import SpaceInvaders as sp
import pygame
game = sp.Game()
class TestUpdateLevel(unittest.TestCase):
    
        
    #def test_file_read(self):
        #print('=====================')
        #print('Test File Read')
        #game.init()
        #print(game.data)
       
    
    #def test_set_level(self):
        #print('=====================')
        #print('Test Set Level')
       # e = game.set_level(1,0)
       # print(len(e))
       # for enemy in e:
       #     print('X Location: ' + str(enemy.x) + ' Y Location: ' + str(enemy.y))
    
    def test_set_level_graphics(self):
        game.init()
        e = game.set_level(1,0)
        win = pygame.display.set_mode((700,700))

        for enemy in e:
            enemy.draw(win)
        pygame.display.update()
        print('Done Drawing Enemies')
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        #print(e)


    
   
        
        
        
        