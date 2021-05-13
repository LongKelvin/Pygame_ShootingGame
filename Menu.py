import sys

from Settings import *
import pygame


class Menu:
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.mid_width = WIDTH / 2
        self.mid_height = HEIGHT / 2
        self.display = True
        self.cursor_rect = pygame.Rect(0, 0, 40, 40)
        self.offset = -120
        self.cursor_rect.x = self.mid_width - 140
        self.cursor_rect.y = self.mid_height - 80
        # offset is gravity of cursor to game text menu

    def draw_cursor(self):
        self.game.draw_text('*', 50, WHITE, self.cursor_rect.x, self.cursor_rect.y)

    def render_to_screen(self):
        # self.game.clock.tick(FPS)
        # self.game.screen.blit(self.game.background, (0, 0))
        pygame.display.update()
        # pygame.display.flip()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx = self.mid_width
        self.starty = self.mid_height - 80
        self.load_gamex = self.mid_width
        self.load_gamey = self.mid_height - 30
        self.savex = self.mid_width
        self.savey = self.mid_height + 20
        self.statx = self.mid_width
        self.staty = self.mid_height + 70
        self.optionx = self.mid_width
        self.optiony = self.mid_height + 120
        self.exitx = self.mid_width
        self.exity = self.mid_height + 170
        self.DOWN_KEY = False
        self.UP_KEY = False
        print("Main menu init")

    def display_menu(self):
        self.display = True
        self.game.play_intro_music()
        while self.display:
            # self.game.events()
            self.events()
            self.game.screen.fill(BLACK)
            self.game.draw_text('Main Menu', 50, GREEN, WIDTH / 2, HEIGHT / 2 - 200)
            self.game.draw_text('Start New Game', 32, WHITE, self.startx, self.starty)
            self.game.draw_text('Load Game ', 32, WHITE, self.load_gamex, self.load_gamey)
            self.game.draw_text('Save Game', 32, WHITE, self.savex, self.savey)
            self.game.draw_text('Stat Player', 32, WHITE, self.statx, self.staty)
            self.game.draw_text('Game Option', 32, WHITE, self.optionx, self.optiony)
            self.game.draw_text('Game Exit', 32, WHITE, self.exitx, self.exity)
            self.draw_cursor()
            self.render_to_screen()

    def update(self):
        # print(self.state)
        for event in pygame.event.get():
            self.game.clock.tick(FPS)
            if event.type == pygame.KEYDOWN:
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_DOWN]:
                    self.DOWN_KEY = True
                    if self.state == "Start":
                        self.cursor_rect.midtop = (self.load_gamex + self.offset, self.load_gamey)
                        self.state = 'Load_game'
                    elif self.state == "Load_game":
                        self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                        self.state = 'Save_game'
                    elif self.state == "Save_game":
                        self.cursor_rect.midtop = (self.statx + self.offset, self.staty)
                        self.state = 'Stat'
                    elif self.state == "Stat":
                        self.cursor_rect.midtop = (self.optionx + self.offset, self.optiony)
                        self.state = 'Option'
                    elif self.state == "Option":
                        self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                        self.state = 'Exit'
                    elif self.state == "Exit":
                        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                        self.state = 'Start'

                if keystate[pygame.K_UP]:
                    self.UP_KEY = True
                    if self.state == "Start":
                        self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                        self.state = 'Exit'
                    elif self.state == "Exit":
                        self.cursor_rect.midtop = (self.optionx + self.offset, self.optiony)
                        self.state = 'Option'
                    elif self.state == "Option":
                        self.cursor_rect.midtop = (self.statx + self.offset, self.staty)
                        self.state = 'Stat'
                    elif self.state == "Stat":
                        self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                        self.state = 'Save_game'
                    elif self.state == "Save_game":
                        self.cursor_rect.midtop = (self.load_gamex + self.offset, self.load_gamey)
                        self.state = 'Load_game'
                    elif self.state == "Load_game":
                        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                        self.state = 'Start'

            if event.type == pygame.KEYDOWN:
                # print("menu event key press")
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_RETURN]:
                    print("Press enter")  # Enter key
                    if self.state == 'Start':
                        self.game.new()
                        self.game.playing = True
                        self.display = False
                        print("new game")
                    elif self.state == 'Load_game':
                        # self.game.curr_menu = self.game.options
                        print("load game")
                    elif self.state == 'Save_game':
                        # self.game.curr_menu = self.game.credits
                        print("save game")

                    elif self.state == 'Stat':
                        # self.game.curr_menu = self.game.credits
                        print("player stats")
                    elif self.state == 'Option':
                        # self.game.curr_menu = self.game.credits
                        print("game option")
                    elif self.state == 'Exit':
                        self.display = False
                        pygame.quit()
                        sys.exit()

    def events(self):
        self.game.clock.tick(FPS)
        self.update()
        # self.display = True
        # while self.display:
        #     for event in pygame.event.get():
        #         self.game.clock.tick(FPS)
        #         if event.type == pygame.KEYDOWN:
        #             print("menu event key press")
        #             keystate = pygame.key.get_pressed()
        #             if keystate[pygame.K_RETURN]:
        #                 print("Press enter")  # Enter key
        #                 if self.state == 'Start':
        #                     self.game.playing = True
        #                     print("new game")
        #                 elif self.state == 'Load_game':
        #                     # self.game.curr_menu = self.game.options
        #                     pass
        #                 elif self.state == 'Save_game':
        #                     # self.game.curr_menu = self.game.credits
        #                     pass
        #                 elif self.state == 'Stat':
        #                     # self.game.curr_menu = self.game.credits
        #                     pass
        #                 elif self.state == 'Option':
        #                     # self.game.curr_menu = self.game.credits
        #                     pass
        #                 elif self.state == 'Exit':
        #                     pygame.quit()
        #
        #                 self.display = False
