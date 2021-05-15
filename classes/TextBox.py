import pygame
from classes.Game import *
from config.Settings import *


class TextBox:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.text = ''
        self.title = ''
        self.selected_value = 0
        self.pos_x = WIDTH / 2  # default position
        self.pos_y = HEIGHT / 2
        self.font_size = FONT_SIZE_NORMAL
        self.font_name = FONTNAME
        self.limit_text_len = 10

    def enter_player_name(self, x, y, font_size=None, title=None):
        self.game.pause = True
        self.game.playing = False
        if not title is None:
            self.title = title
        else:
            self.title = "Enter player name: "

        # Loop game
        if not self.game.running:
            return
        while self.game.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game.player_name = self.text
                        print("input text:" + self.text)
                        self.text = ''
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        if len(self.text) < self.limit_text_len:
                            self.text += event.unicode

            self.game.screen.fill(BLACK)


            if not font_size is None:
                self.font_size = font_size
            # draw to screen
            self.game.draw_text(self.title, self.font_size, WHITE, x, y)
            self.game.draw_text(self.text, self.font_size, GREEN, x + 250, y)

            pygame.display.flip()
            self.game.clock.tick(FPS)

    def enter_file_name(self, x, y, font_size=None, title=None):
        self.game.pause = True
        self.game.playing = False
        if not title is None:
            self.title = title
        else:
            self.title = "Enter file name: "

        # Loop game
        if not self.game.running:
            return
        while self.game.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game.file_name = self.text + '.txt'
                        print("input text:" + self.text)
                        self.text = ''
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        if len(self.text) < self.limit_text_len:
                            self.text += event.unicode

            self.game.screen.fill(BLACK)

            if not font_size is None:
                self.font_size = font_size
            # draw to screen
            self.game.draw_text(self.title, self.font_size, WHITE, x, y)
            self.game.draw_text(self.text, self.font_size, GREEN, x + 250, y)

            pygame.display.flip()
            self.game.clock.tick(FPS)

    def enter_user_selected_input(self):
        pass
