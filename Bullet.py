
from Settings import *
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
        self.image = bullet_img
        # self.image.fill(YELLOW)
        # self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        # print("Bullet has init complete")

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
