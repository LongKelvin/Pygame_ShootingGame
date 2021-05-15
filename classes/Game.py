import pygame
import random

from animation.Explosion import Explosion
from animation.PowerUp import PowerUp
from classes.Menu import MainMenu, PauseGameMenu, GameLoad_Menu

from classes.TextBox import TextBox

from config.Settings import*
from enemy.Mob import Mob

import os


from player.Player import Player


class Game:
    def __init__(self):
        # init game
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.all_sprites = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONTNAME)
        self.load_data()
        self.player_name = 'player'
        self.pause = False
        self.score = 0
        self.player = Player(self)
        self.playing = False
        self.file_data = []
        self.file_name = 'game_data_.txt'
        self.winning = False
        self.winning_bar = 0
        self.list_save_data = os.listdir(game_data_dir)
        self.main_menu = MainMenu(self)
        self.game_load_menu = GameLoad_Menu(self)
        self.pause_menu = PauseGameMenu(self)
        self.current_menu = self.main_menu

    def load_data(self):
        # load background image
        self.background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
        self.background_rect = self.background.get_rect()

        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.player_mini_img = pygame.transform.scale(player_img, (25, 19))
        self.player_mini_img.set_colorkey(BLACK)
        # load sound and music
        # Load all game sound and music
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
        self.expl_sounds = []
        for snd in ['expl3.wav', 'expl6.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
        self.player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
        self.powerup_shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
        self.powerup_gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
        # pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        # pygame.mixer.music.set_volume(0.25)
        # pygame.mixer.music.play(loops=-1)
        self.player_hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hitmob.wav'))

    def newmob(self):
        m = Mob()
        self.all_sprites.add(m)
        self.mobs.add(m)

    def play_background_music(self, loop=-1, volume=0.5):
        pygame.mixer.music.load(path.join(snd_dir, 'background.wav'))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)

    def play_intro_music(self):
        pygame.mixer.music.load(path.join(snd_dir, 'game_start_music.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def new(self, player_lives=None, player_score=None, player_shield=None):
        # start a new game
        self.play_background_music(-1)
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = Player(self)
        if not player_score is None:
            self.score = player_score
        if not player_shield is None:
            self.player.shield = player_shield
        if not player_lives is None:
            self.player.lives = player_lives

        self.bullets = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        for i in range(10):
            m = Mob()
            self.all_sprites.add(m)
            self.mobs.add(m)

        self.run()

    def run(self):
        # Game loop
        # Check background music
        self.playing = True
        self.pause = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.pause:
                self.update()
                self.draw()

    def update(self):
        # Game loop sprites update
        global death_explosion
        self.all_sprites.update()

        # hit mob ...
        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.score += 50
            random.choice(self.expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            self.all_sprites.add(expl)
            if random.random() > 0.3:  # mean that the percent is 9%
                powerUp = PowerUp(hit.rect.center)
                self.all_sprites.add(powerUp)
                self.powerups.add(powerUp)
            self.newmob()

        # check to see if a mob hit the player
        # hits = pygame.sprite.spritecollide(player, mobs, False)

        hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            self.all_sprites.add(expl)
            self.newmob()
            self.player_hit_sound.play()

            if self.player.shield <= 0:
                death_explosion = Explosion(hit.rect.center, 'player')
                self.all_sprites.add(death_explosion)
                self.player.lives -= 1
                self.player.shield = 100
                self.player_die_sound.play()
                self.player.hide()

        # check if player hit the powerup
        hit_player_powerup = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hit_player_powerup:
            if hit.type == 'shield':
                self.player.shield += random.randrange(10, 30)
                self.powerup_shield_sound.play()
                if self.player.shield >= 100:
                    self.player.shield = 100
                # for mob in self.mobs:
                #     mob.kill()
                #     expl = Explosion(hit.rect.center, 'lg')
                #     self.all_sprites.add(expl)
                #
                # self.score += 1000
                # for index in range(10):
                #     self.newmob()

            elif hit.type == 'gun':
                self.player.powerup()
                self.powerup_gun_sound.play()
        # if player die and the death_explosion has finish
        if self.player.lives == 0 and not death_explosion.alive():
            self.player_die_sound.play()
            self.playing = False

        # if self.score in range(WIN_SCORE - 300, WIN_SCORE):
        #     self.play_intro_music()

        # WINNING SECTION
        if self.score >= WIN_SCORE:
            now = pygame.time.get_ticks()
            self.winning = True
            # pygame.mixer.music.stop()
            # self.clock.tick(FPS_SLOWING)

            print(now)
            self.player.rect.y = HEIGHT / 2 - 100
            self.player.rect.x = WIDTH / 2
            hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                self.player.shield = self.player.shield
                expl = Explosion(hit.rect.center, 'lg')
                self.all_sprites.add(expl)
                random.choice(self.expl_sounds).play()
            for mob in self.mobs:
                mob.kill()
                expl = Explosion(mob.rect.center, 'lg')
                self.all_sprites.add(expl)

                for sound in self.expl_sounds:
                    sound.play()

            for power in self.powerups:
                expl = Explosion(power.rect.center, 'lg')
                self.all_sprites.add(expl)
                power.kill()
            if now > GAME_WINNING_TIME:
                self.show_winner_screen()

    def events(self):
        # Get input event
        for event in pygame.event.get():
            # check for window closing
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    # self.show_pause_screen()
                    self.current_menu = self.pause_menu
                    self.current_menu.display_menu()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text("Score:  " + str(self.score), 18, WHITE, WIDTH / 2, 10)
        self.draw_text("Player shield:  ", 18, WHITE, 70, 0)
        self.draw_text("Lives:  ", 18, WHITE, WIDTH - 150, 5)
        if not self.player.shield is None:
            self.draw_shield_bar(10, 25, self.player.shield)
        self.draw_lives(WIDTH - 100, 5, self.player.lives, self.player_mini_img)
        self.draw_text("Player:  ", 18, WHITE, WIDTH - 145, 30)
        self.draw_text(self.player_name, 20, GREEN, WIDTH - 65, 30)
        pygame.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def show_go_screen(self):
        # game over/continue
        pygame.mixer.music.stop()
        self.play_intro_music()
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def show_winner_screen(self):
        # game winner screen
        self.clock.tick(FPS)
        # pygame.mixer.music.stop()
        self.play_intro_music()
        if not self.running:
            return
        # self.screen.fill(BLACK)
        now = pygame.time.get_ticks()
        self.draw_text("YOU WIN", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("High Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        pygame.display.flip()
        # if pygame.time.get_ticks() -  now > GAME_DELAY_EVENT:
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
        self.current_menu.display_menu()

    # draw text
    def draw_text(self, text, size, color, x, y):
        pygame.init()
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        try:
            self.screen.blit(text_surface, text_rect)
        except:
            print("game surface can't display")

    def draw_shield_bar(self, x, y, percent):
        if percent < 0:
            percent = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (percent / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, GREEN, fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

    def draw_game_winning_bar(self, x, y, percent):
        if percent < 0:
            percent = 0
        BAR_LENGTH = WIDTH - 100
        BAR_HEIGHT = HEIGHT / 8
        fill = (percent / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, GREEN, fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

    def draw_lives(self, x, y, lives, image):
        for index in range(lives):
            img_rect = image.get_rect()
            img_rect.x = x + 30 * index
            img_rect.y = y
            self.screen.blit(image, img_rect)

    def load_game_from_file(self, filename):
        game_data = open(path.join(game_data_dir, filename), 'r')
        data = game_data.read().splitlines()
        print(data)
        self.new(int(data[0]), int(data[1]), int(data[2]))
        self.show_go_screen()

    def save_game_data(self, filename, g_data):
        # game data include player lives, shield and score
        save_file = open(path.join(game_data_dir, filename), 'w+')
        for data in g_data:
            save_file.write(str(data) + '\n')

    def show_input_name(self, font_size=None):
        textbox = TextBox(self)
        textbox.enter_player_name(WIDTH / 4, HEIGHT / 2, font_size)

    def show_input_filename(self, font_size=None):
        self.draw_text('Save Game', 50, GREEN, WIDTH / 2, HEIGHT / 2 - 200)
        textbox = TextBox(self)
        textbox.enter_file_name(WIDTH / 4, HEIGHT / 2, font_size)

    def get_game_data(self):
        self.file_data.append(self.player.lives, )
        self.file_data.append(self.score)
        self.file_data.append(self.player.shield, )
        self.file_data.append(self.player_name)

    def update_list_save_data(self):
        self.list_save_data = os.listdir(game_data_dir)
