import unittest
import pygame
from platformer import Player, Platform

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Initialize pygame for sprite handling (needed for rects)
        pygame.init()
        self.player = Player(100, 100)
        self.platforms = pygame.sprite.Group()
        # Add a floor
        self.floor = Platform(0, 200, 800, 20)
        self.platforms.add(self.floor)

    def test_gravity(self):
        initial_y = self.player.rect.y
        self.player.update(self.platforms)
        # Player should fall (y increases)
        self.assertGreater(self.player.rect.y, initial_y)

    def test_collision_floor(self):
        # Place player right above floor
        self.player.rect.bottom = self.floor.rect.top - 1
        self.player.change_y = 10 # Moving down

        self.player.update(self.platforms)

        # Player should be on top of floor
        self.assertEqual(self.player.rect.bottom, self.floor.rect.top)
        self.assertTrue(self.player.on_ground)
        self.assertEqual(self.player.change_y, 0)

    def test_movement(self):
        initial_x = self.player.rect.x
        self.player.go_right()
        self.player.update(self.platforms)
        self.assertGreater(self.player.rect.x, initial_x)

        self.player.stop()
        self.player.go_left()
        self.player.update(self.platforms)
        # Should be back to near initial x (depends on speed)
        # We just want to check direction
        self.assertEqual(self.player.change_x, -5)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
