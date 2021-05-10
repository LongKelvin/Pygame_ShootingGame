# pygame template
import pygame
import random
from os import path

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
    YELLOW = (255, 255, 0)
    # set up assets folders
    img_dir = path.join(path.dirname(__file__), 'img')

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

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((30, 40))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 20))
            self.image.fill(YELLOW)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            # kill if it moves off the top of the screen
            if self.rect.bottom < 0:
                self.kill()


    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        # Update
        all_sprites.update()

        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            running = False

        # Draw/ Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        # draw buffer
        pygame.display.flip()

    pygame.quit()
