import unittest
import SpaceInvaders as sp

game = sp.Game()
class TestUpdateLevel(unittest.TestCase):
    def test_file_read(self):
        game.init()
        print(game.data)
        
    def test_set_level(self):
        e = game.set_level(1, 0)
        print(e)
        
    def test_placement_single_enemy(self):
        pass
        