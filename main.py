from Game import *
from Menu import *

game = Game()
# game.show_start_screen()
# game.input_text(24)
# game.show_pause_screen()
all_data = os.listdir(game_data_dir)
# game.show_game_list_data(all_data)

while game.running:
    # game.load_game_from_file(path.join(game_data_dir, 'game_data.txt'))
    # data = ['1', '200', '50']
    # game.save_game_data(path.join(game_data_dir, 'game_new_data.txt'),data)
    # game.input_text(40)
    game.current_menu.display_menu()
    game.show_go_screen()

pygame.quit()
