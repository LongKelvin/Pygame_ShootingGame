# pygame template

import pygame

if __name__ == '__main__':
    WIDTH = 360
    HEIGHT = 480
    FPS = 30

    # define color
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    # init pygame and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(WIDTH, HEIGHT)
    pygame.display.set_caption("Shooting_Game")
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        # Process input (event)
        for event in pygame.event.get():
            # check quit game
            if event.type == pygame.QUIT:
                running = False

        # Update
        # Render
        screen.fill(BLACK)

        # draw buffer
        pygame.display.flip()
