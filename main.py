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
    snd_dir = path.join(path.dirname(__file__), 'snd')
    # init pygame and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooting_Game")
    clock = pygame.time.Clock()

    # Load all game graphics
    background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
    background_rect = background.get_rect()
    player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    meteor_images = []
    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
                   'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
                   'meteorBrown_tiny1.png']
    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    explosion_animation = {'lg': [], 'sm': []}
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_animation['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_animation['sm'].append(img_sm)
    # Load all game sound and music
    print(snd_dir)
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    expl_sounds = []
    for snd in ['expl3.wav', 'expl6.wav']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.25)

    # font for game
    # font_name = pygame.font.SysFont(None, 20)
    font_name = pygame.font.match_font("arial")

    # draw text
    def draw_text(surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)


    def newmob():
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


    def draw_shield_bar(surface, x, y, percent):
        if percent < 0:
            percent = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (percent / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    # Game object
    class Player(pygame.sprite.Sprite):
        # sprite for the player
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # self.image = pygame.Surface((50, 40))
            # self.image.fill(GREEN)
            self.image = pygame.transform.scale(player_img, (50, 38))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            # set radius to improve collision with mob
            self.radius = 20
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = (HEIGHT - 10)
            self.speedx = 0
            self.shield = 100
            self.shoot_delay = 250
            self.last_shoot = pygame.time.get_ticks()

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_w] or keystate[pygame.K_UP]:
                self.rect.top -= 5
            if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
                self.rect.bottom += 5
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shoot > self.shoot_delay:
                self.last_shoot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()


    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # self.image = pygame.Surface((30, 40))
            self.image_orig = random.choice(meteor_images)
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig.copy()
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
            self.radius = int(self.rect.width * .85 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
            self.last_update = pygame.time.get_ticks()

        def rotate(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                # rotate the mob
                self.rot = (self.rot + self.rot_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center

        def update(self):
            self.rotate()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            # self.image = pygame.Surface((10, 20))
            self.image = bullet_img
            # self.image.fill(YELLOW)
            # self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            # kill if it moves off the top of the screen
            if self.rect.bottom < 0:
                self.kill()


    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = explosion_animation[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_animation[self.size]):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = explosion_animation[self.size][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center


    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    score = 0
    pygame.mixer.music.play(loops=-1)
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
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         player.shoot()
        # Update
        all_sprites.update()

        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            newmob()

        # check to see if a mob hit the player
        # hits = pygame.sprite.spritecollide(player, mobs, False)
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            newmob()
            if player.shield <= 0:
                running = False

        # Draw/ Render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, "Score:  " + str(score), 18, WIDTH / 2, 10)
        draw_text(screen, "Player shield:  ", 18, 0, 0)
        draw_shield_bar(screen, 5, 20, player.shield)
        # draw buffer
        pygame.display.flip()

    pygame.quit()
