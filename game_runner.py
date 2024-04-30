"""
    Name: Rahik N Sikder
    UTEID: rns2359

    On my honor, RAHIK N SIKDER, this programming assignment is my own work
    and I have not provided this code to any other student.

    Complete the following:
    
    0. sikder.rahik@gmail.com

    1. The purpose of my program is to provide a tool to start messing around with Card Counting
        The project has been made through an object oriented paradigm to allow an effective
        simulation of real world cards and greater ease to write with future updates and run my
        own tests. The ability to tweak the playing conditions and display the information I find
        useful is the major appeal of creating this program over using card counting programs
        already published on the web.

    2. The major feature of my program is that the Blackjack game is able to display information
        about the running count, or the count directly taken from the cards on the table, and the 
        true count, the count divided by the number of decks in the shoe and the one advantage
        players use to guide bet strategy. In a one deck shoe, the running count should equal the
        true count, however since casino almost never use a one deck shoe, this program does not
        try to handle cases with small shoe sizes.

        Also, the program has a functioning Blackjack game and there are artifical delays with each
        computer bot's turn to emulate mutitple players. The number of players, as well as the shoe
        size, can be altered through the Blackjack() constructor in declare_globals(). The split
        action is a part of Blackjack not yet implemented; however, I felt it's importance is
        not that significant when the primary purpose of this program is for card counting.

    3. The only external module should be pygame. 
        Run with the command 'pip install pygame' or 'pip3 install pygame'
        On my system, since I use the Homebrew Package Manager with multiple python, I had to
        specifically run 'pip3.12 install pygame --break-system-packages'

        I wrote a script that fetchs jpg cards from the website
        http://www.marytcusack.com/maryc/Cards/index.html
        If you want to play around with this script and try out other card decks you would need to
        have the requests module installed using 'pip install requests', 'pip3 install requests' or
        'pip3.12 install requests --break-system-packages'

    4. This project forced me to really think about object oriented design and knowing that this 
        would be a project I am actually set on fully completing, I wanted to design this correctly
        from the groud up. If you look into the card_deck.py file, you'll find a lot of code that
        could be condensed into a few functions or even a single class. However, this approach 
        could limit any future features I may want to implement and I had to learn how to write 
        this program keeping that in mind. This is why I've implemented types for some key 
        parameters, just to make sure the code is readable and ultimately maintainable.

        I also had to learn pygame from scratch, which ended up not being too difficult. The pygame
        experience is much more seemless than tkinter hell, and there are a lot of resources 
        online. The boilerplate code for this main game loop is linked below. This project honestly
        felt more like a project from CS 314 than it did an Intro Python class project. 
    
    5. Pygame, despite me claiming it's ease of use above, was still the largest obstacle to this
        project. After getting a basic Blackjack game running, I spent most of my hours on the 
        graphical side of this project, and only after finishing that did I go back to the game 
        logic and implement proper card counting.

    6. The first thing I would add is a proper menu. As the terminal output when you run this 
        program states, in order to change the shoe size and number of players (bots), you need to
        manually change the constructor for the Blackjack() object which holds the game logic. 

        After that, I would add more card counting schemes, essentially switching between different
        mappings for each card's weight. Additionally, I would tighten up the game logic, which
        entails properly implementing a split function for the user and player bots. Also a label
        that says if the Dealer beat you and how much money you gained or lost in that round.

        From here comes simulations and being able to use this program as a blackjack simulation for
        thousands of game cycles. The Blackjack class would need to be modified, copying some of
        the draw functions to simply return a value that can be stored and displayed over many 
        game cycles. 


Credit for pygame boiler plate: https://gist.github.com/MarquisLP/b534c95e4a11efaf376e
"""

import sys
import pygame
from pygame.locals import *

# Import additional modules here.
from card_deck import *
from game_engine import *

# Feel free to edit these constants to suit your requirements.
FRAME_RATE = 60.0
SCREEN_SIZE = (1400, 800)


class Button:
    """
    Class created to render a button on screen.
    """

    def __init__(self, screen, x, y, run_function, text, width=100, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text: str = text
        self.run_function = run_function

        self.surface = screen
        self.surface.fill((52, 61, 70))

        self.font = pygame.font.Font(None, 35)
        self.text_surface = self.font.render(text, True, (255, 255, 255))

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        color = (52, 61, 70)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = (79, 91, 102)

        pygame.draw.rect(self.surface, color, self.rect, 0, 10)
        screen.blit(self.text_surface, (self.x + 15, self.y + 15))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.run_function(self.text.strip())
                return True
        return False


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
    # Style: Treating methods as if they are inside of a class

    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Card Counting Coach")
    clock = pygame.time.Clock()

    def declare_globals():
        # The class(es) that will be tested should be declared and initialized
        # here with the global keyword.
        # Yes, globals are evil, but for a confined test script they will make
        # everything much easier. This way, you can access the class(es) from
        # all three of the methods provided below.

        global blackjack
        blackjack = Blackjack(game_screen, num_bots=4)

        global press_hit
        global press_stand
        global press_split
        global new_round

        but_pos = (300, 150)
        press_hit = Button(
            game_screen, but_pos[0], but_pos[1], blackjack.play_round, "  Hit  "
        )
        press_stand = Button(
            game_screen, but_pos[0] + 120, but_pos[1], blackjack.play_round, "Stand"
        )
        press_split = Button(
            game_screen, but_pos[0] + 240, but_pos[1], blackjack.play_round, "Split"
        )
        new_round = Button(
            game_screen,
            but_pos[0] + 90,
            but_pos[1] + 70,
            blackjack.new_round_start,
            "New Round",
            width=170,
            height=50,
        )

    def prepare_game():
        # Add in any code that needs to be run before the game loop starts.

        # Start the first new round
        blackjack.new_round_start(0)

    def update(screen, time):
        game_screen.fill((101, 115, 126))

        # Draw title
        title_font = pygame.font.Font(None, 85)
        subtitle_font = pygame.font.Font(None, 35)
        title = title_font.render("Card Counting Coach", True, (255, 255, 255))
        subtitle = subtitle_font.render("Rahik Sikder", True, (255, 255, 255))
        game_screen.blit(title, (50, 50))
        game_screen.blit(subtitle, (50, 120))

        # Draw buttons
        press_hit.draw(game_screen)
        press_stand.draw(game_screen)
        press_split.draw(game_screen)
        new_round.draw(game_screen)
        blackjack.draw_bet_slider()

        # Draw shoe, dealer, and players
        blackjack.draw_shoe()
        blackjack.draw_players()

        # Draw the count and true count
        blackjack.draw_count()
        blackjack.draw_true_count()

        if blackjack.current_player == blackjack.num_players - 1 and time >= (
            blackjack.cur_time + 1
        ):
            # Dealer plays
            move_on = blackjack.dealer_play()
            if move_on:
                blackjack.evaluate_round()
                blackjack.current_player = 0
            blackjack.cur_time = time

        elif (
            not blackjack.is_player_turn
            and not blackjack.game_over
            and time >= (blackjack.cur_time + 1)
        ):
            blackjack.current_player += 1
            move_on = blackjack.bot_play_round(blackjack.current_player)
            blackjack.current_player -= 0 if move_on else 1
            blackjack.cur_time = time

        elif blackjack.is_player_turn or blackjack.game_over:
            blackjack.cur_time = time

        pygame.display.update()

    def main():
        print(
            "**********************************************************************************"
        )
        print("About the project:")
        print(
        "Currently there is no menu to set the shoe size or number of bots prior to the game loop"
        )
        print(
            "This can be done manually in the Blackjack() game constructor with the named "
        )
        print("fields: num_bots and shoe_size")
        print(
            "Additionally, this means that when the shoe is depleted the window will close."
        )
        print(
            "**********************************************************************************"
        )

        declare_globals()
        prepare_game()
        start_tick = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)

                press_hit.is_clicked(event)
                press_stand.is_clicked(event)
                press_split.is_clicked(event)
                new_round.is_clicked(event)
                blackjack.check_bet_slider(event)

            milliseconds = clock.tick(FRAME_RATE)
            seconds = (pygame.time.get_ticks() - start_tick) / 1000
            update(game_screen, seconds)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

    main()
