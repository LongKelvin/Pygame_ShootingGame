from classes.Game import *
from classes.TextBox import *




game = Game()

while game.running:
    game.current_menu.display_menu()
    game.show_go_screen()
pygame.quit()
