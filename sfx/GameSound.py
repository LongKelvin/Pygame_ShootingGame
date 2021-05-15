import pygame

from Settings import *


class Sound:
    def __init__(self):
        # Load all game sound and music
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
        self.expl_sounds = []
        for snd in ['expl3.wav', 'expl6.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
            player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
        self.powerup_shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
        self.powerup_gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))

    def play_background_music(self, loop=-1, volume=0.25):
        pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
