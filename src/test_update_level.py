import unittest
import SpaceInvaders as sp

game = sp.Game()
class TestUpdateLevel(unittest.TestCase):
    
    def test_file_read(self):
        #print('=====================')
        #print('Test File Read')
        game.init()
        #print(game.data)
       
    
    def test_set_level(self):
        #print('=====================')
        #print('Test Set Level')
        e = game.set_level(1,0)
        #print(e)
    
    def test_set_enemy_locations(self):
        print('=========================')
        print('Test Set Enemy Locations')
        e = game.set_level(1,0)
        e = game._set_enemy_locations(e)
       # print(len(e))
        print("=====+++++=======")
        
        
        
        