# pygame template

import pygame
import random
import os

if __name__ == '__main__':
    WIDTH = 800
    HEIGHT = 600
    FPS = 60

    # define color
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    # set up assets folders
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, "img")

    # init pygame and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooting_Game")
    clock = pygame.time.Clock()


    # Game object
    class Player(pygame.sprite.Sprite):
        # sprite for the player
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = (HEIGHT - 10)
            self.speedx = 0

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0


    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (event)
        for event in pygame.event.get():
            # check quit game
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # Draw/ Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        # draw buffer
        pygame.display.flip()

    pygame.quit()
