import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simple Platformer"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = BLUE
MOVE_SPEED = 5
JUMP_FORCE = 12
GRAVITY = 0.8

# Platform properties
PLATFORM_COLOR = GREEN

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

    def update(self, platforms):
        # Gravity
        self.change_y += GRAVITY

        # Move left/right
        self.rect.x += self.change_x

        # Horizontal Collision
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Vertical Collision
        self.on_ground = False
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.on_ground = True
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0

    def jump(self):
        if self.on_ground:
            self.change_y = -JUMP_FORCE

    def go_left(self):
        self.change_x = -MOVE_SPEED

    def go_right(self):
        self.change_x = MOVE_SPEED

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Create Player
    player = Player(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 20)
    all_sprites.add(player)

    # Create Platforms
    # (x, y, width, height)
    level_platforms = [
        [0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20],  # Floor
        [200, 450, 200, 20],
        [500, 350, 200, 20],
        [100, 250, 150, 20],
        [400, 150, 100, 20]
    ]

    for plat in level_platforms:
        block = Platform(plat[0], plat[1], plat[2], plat[3])
        platforms.add(block)
        all_sprites.add(block)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()

        # Handle key presses for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.go_left()
        elif keys[pygame.K_RIGHT]:
            player.go_right()
        else:
            player.stop()

        # Update
        player.update(platforms)

        # Draw
        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
