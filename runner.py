"""This module contains all of the necessary PyGame components for
running a simplified game loop.
Use it for test cases on PyGame-related code.
"""
import sys
import pygame
from pygame.locals import *
# Import additional modules here.
from card_deck import *
from game_engine import *

# Feel free to edit these constants to suit your requirements.
FRAME_RATE = 60.0
SCREEN_SIZE = (1600, 900)


def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Card Counting Coach')
    clock = pygame.time.Clock()

    def declare_globals():
        # The class(es) that will be tested should be declared and initialized
        # here with the global keyword.
        # Yes, globals are evil, but for a confined test script they will make
        # everything much easier. This way, you can access the class(es) from
        # all three of the methods provided below.
        global deck 
        deck = CardDeck()
        global blackjack
        blackjack = BlackJack(game_screen, num_bots=3)
        blackjack.new_round_start()
        pass

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        pass

    def handle_input(key_name):
        # Add in code for input handling.
        # key_name provides the String name of the key that was pressed.
        pass

    def update(screen, time):
        game_screen.fill((79,91,102))

        # Draw title
        title_font = pygame.font.Font(None, 85)
        subtitle_font = pygame.font.Font(None, 35)
        title = title_font.render("Card Counting Coach", True, (255, 255, 255))
        subtitle = subtitle_font.render("Rahik Sikder", True, (255, 255, 255))
        game_screen.blit(title, (50, 50))
        game_screen.blit(subtitle, (50, 120))


        blackjack.draw_players()

        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
        pygame.display.update()

    # Add additional methods here.

    def main():
        declare_globals()
        prepare_test()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)

            milliseconds = clock.tick(FRAME_RATE)
            seconds = milliseconds / 1000.0
            update(game_screen, seconds)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

    main()