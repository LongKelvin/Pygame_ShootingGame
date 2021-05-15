import pygame
import random
from config.Settings import *

from weapon.Bullet import *



class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self, game):
        self.game = game
        self.group = game.all_sprites
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
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
        self.lives = 3
        self.hidden = False
        self.hidden_time = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        # print("Player has init complete")

    def update(self):
        # time out for power up
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWER_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # unhidden if hidden
        if self.hidden and pygame.time.get_ticks() - self.hidden_time > 2000:
            self.hidden = False
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0


        try:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -6
            if keystate[pygame.K_RIGHT]:
                self.speedx = 6
            if keystate[pygame.K_w] or keystate[pygame.K_UP]:
                self.rect.top -= 6
            if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
                self.rect.bottom += 6
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                if self.hidden:
                    self.rect.bottom = HEIGHT + 100
                else:
                    self.rect.bottom = HEIGHT
        except:
            print('Something went wrong in player event')

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.game.all_sprites.add(bullet)
                self.game.bullets.add(bullet)
                self.game.shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                self.game.shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
