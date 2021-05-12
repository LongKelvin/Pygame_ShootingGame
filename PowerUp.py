import random
from settings import *


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        self.powerup_images = {'shield': pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert(),
                               'gun': pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()}
        self.type = random.choice(['shield', 'gun'])
        self.image = self.powerup_images[self.type]
        # self.image.fill(YELLOW)
        # self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5
        print("Powerup has init complete")

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

    def load_image(self):
        pass
