from card_deck import *
from typing import List
import pygame
from pygame.locals import *

# A few Constants
CARD_SIZE = 115
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (250, 123, 123)


# Typical card counting system
HIGH_LOW_COUNT = {
    1: -1,  # A
    2: 1,  # 2
    3: 1,  # 3
    4: 1,  # 4
    5: 1,  # 5
    6: 1,  # 6
    7: 0,  # 7
    8: 0,  # 8
    9: 0,  # 9
    10: -1,  # 10, J, Q, K
}


class Player:

    def __init__(
        self, name, screen, position, stack=500, is_dealer=False, bot_level=0
    ) -> None:
        # Drawing
        self.screen = screen
        self.position: tuple = position
        # Game Info
        self.name = name
        self.is_dealer = is_dealer
        self.bot_level = bot_level
        self.current_cards: List[Card] = []
        self.value = 0
        self.is_bust = False
        self.stack = stack
        self.bot_move_label = ""
        self.ace_count = 0
        self.bet_size = 25

    def make_guess(self) -> str:
        if self.is_dealer:
            # Dealer ai
            move = "Hit" if self.value < 17 else "Stand"
        elif self.bot_level > 0:
            move = "Hit" if self.value < 17 or random.randint(1, 10) < 2 else "Stand"
        else:
            move = random.choice(["Hit", "Stand"])
        self.bot_move_label = "| " + move + " |"
        return move

    def take_card(
        self,
        card: Card,
    ) -> None:
        # TODO: Dealer's second Ace Case
        # Ace special count
        if card.value == 1:
            self.ace_count += 1
            self.value += 11
        else:
            self.value += card.value

        self.is_bust = self.value > 21

        # Ace case cont
        if self.is_bust and self.ace_count > 0:
            self.is_bust = False
            self.ace_count -= 1
            self.value -= 10

        self.current_cards.append(card)

    def clear_hand(self) -> None:
        self.current_cards: List[Card] = []
        self.value = 0
        self.is_bust = False
        self.bot_move_label = ""
        self.ace_count = 0

    def draw_player(self) -> None:
        offset = 0
        name_font = pygame.font.Font(None, 24)
        color = COLOR_WHITE if not self.is_bust else COLOR_RED
        # Name tag + Stack
        name_tag = name_font.render(
            self.name + " Stack: " + str(self.stack), True, color
        )
        self.screen.blit(name_tag, (self.position[0], self.position[1]))
        # Hit / Stand
        action_tag = name_font.render(self.bot_move_label, True, color)
        self.screen.blit(action_tag, (self.position[0], self.position[1] - 20))

        for card in self.current_cards:
            cardImage = pygame.transform.scale(
                pygame.image.load(card.png), (CARD_SIZE, CARD_SIZE * 1.61)
            )
            # Create a surface for the card with a border
            bordered_surface = pygame.Surface(
                (cardImage.get_width() + 2, cardImage.get_height() + 2)
            )
            bordered_surface.fill((0, 0, 0))  # Fill the surface with black
            bordered_surface.blit(
                cardImage, (1, 1)
            )  # Blit the card image onto the surface with an offset of 1 pixel

            # Draw the bordered card onto the screen
            self.screen.blit(
                bordered_surface,
                (self.position[0] + offset, self.position[1] + 20 + offset / 2),
            )
            offset += 30


class Blackjack:

    def __init__(self, screen, shoe_size=4, num_bots=0) -> None:
        # Drawing
        self.screen = screen
        self.dragging_slider = False
        # Game Info
        num_bots = min(6, num_bots)  # Max of 7 players
        self.num_players = 1 + num_bots
        self.shoe = Shoe(shoe_size)
        self.running_count = 0
        self.true_count = 0
        self.cur_time = 0  # Stalls when a card is selected
        self.is_player_turn = True
        self.game_over = False
        self.current_player = 0
        self.dealer = Player("Dealer", screen, (750, 100), is_dealer=True)
        self.players: List[Player] = [Player("Your", screen, (75, 250))]
        for i in range(min(6, num_bots)):
            self.players.append(
                Player(
                    f"Bot {i+1}",
                    screen,
                    (((800 / num_bots) + i * (1200 / num_bots)), 535),
                    bot_level=i,
                )
            )

    def new_round_start(self, placeholder_param):
        self.dealer.clear_hand()
        self.deal_card(self.dealer, face_up=False)
        self.deal_card(self.dealer)
        for player in self.players:
            player.clear_hand()
            self.deal_card(player)
            self.deal_card(player)
        self.is_player_turn = True
        self.current_player = 0
        self.game_over = False

    def play_round(self, action: str) -> str:
        """
        If it's the player's turn they can choose to Hit or Stand.
        TODO: Functionality for Splitting
        """
        if not self.is_player_turn:
            return "Not Your Turn"

        elif self.players[0].is_bust:
            return "Bust"

        elif action == "Stand":
            self.is_player_turn = False
            return "Stand"

        elif action == "Split":
            print("Sorry, functionality not yet implemented")
            return "Stood"

        elif action == "Hit":
            self.deal_card(self.players[0])
            self.is_player_turn = not self.players[0].is_bust
            return "Hit"

    def bot_play_round(self, i) -> None:
        cur_bot: Player = self.players[i]
        if not cur_bot.is_bust and cur_bot.make_guess() == "Hit":
            self.deal_card(cur_bot)
            return False
        return True

    def dealer_play(self) -> None:
        # Reveal the dealer's card
        if not self.dealer.current_cards[0].is_visible:
            self.dealer.current_cards[0].flip()
            self.__update_count(self.dealer.current_cards[0].value)
            return False
        # Play as dealer
        if not self.dealer.is_bust and self.dealer.make_guess() == "Hit":
            self.deal_card(self.dealer)
            return False
        return True

    def evaluate_round(self) -> str:
        for player in self.players:
            if player.value > 21 or (not self.dealer.is_bust and player.value < self.dealer.value):
                player.stack -= player.bet_size
            elif player.value > self.dealer.value:
                player.stack += player.bet_size
        self.game_over = True

    def deal_card(self, player: Player, face_up=True):
        card = self.shoe.take_card()
        if face_up:
            card.flip()
            self.__update_count(card.value)
        player.take_card(card)

    def __update_count(self, value):
        self.running_count += HIGH_LOW_COUNT[value]
        self.true_count = round(self.running_count * 52 / self.shoe.length())

    def draw_players(self) -> None:
        self.dealer.draw_player()
        for player in self.players:
            player.draw_player()

    def draw_shoe(self) -> None:
        offset = 0
        # Display shoe size
        name_font = pygame.font.Font(None, 24)
        shoe_tag = name_font.render(
            f"Shoe size is {self.shoe.length()}", True, COLOR_WHITE
        )
        self.screen.blit(shoe_tag, (1200, 50))
        shoe_tag = name_font.render(
            f"Approx {round(self.shoe.length() / 52)} decks", True, COLOR_WHITE
        )
        self.screen.blit(shoe_tag, (1200, 75))
        for card in self.shoe.cards[:30]:
            cardImage = pygame.transform.scale(
                pygame.image.load(card.png), (CARD_SIZE, CARD_SIZE * 1.6)
            )
            # Create a surface for the card with a border
            bordered_surface = pygame.Surface(
                (cardImage.get_width() + 2, cardImage.get_height() + 2)
            )
            bordered_surface.fill((0, 0, 0))  # Fill the surface with black
            bordered_surface.blit(
                cardImage, (1, 1)
            )  # Blit the card image onto the surface with an offset of 1 pixel

            # Draw the bordered card onto the screen
            self.screen.blit(
                bordered_surface,
                (1200 + offset, 100),
            )
            offset += 5

    def draw_count(self):
        # Define the coordinates and dimensions of the box
        x, y = 975, 100
        width, height = 200, 50

        # Create a rect for the box
        true_count_rect = pygame.Rect(x, y, width, height)

        # Check if the mouse is hovering over the box
        if true_count_rect.collidepoint(pygame.mouse.get_pos()):
            # Draw the box with a light blue color
            pygame.draw.rect(self.screen, (173, 216, 230), true_count_rect)

            # Render and display the true count text
            font = pygame.font.Font(None, 24)
            true_count_text = font.render(
                f"Running Count: {self.running_count}", True, (0, 0, 0)
            )
            self.screen.blit(true_count_text, (x + 10, y + 10))
        else:
            # Draw the box with a dark blue color
            pygame.draw.rect(self.screen, (0, 0, 128), true_count_rect)

            # Render and display the label "True Count"
            font = pygame.font.Font(None, 24)
            true_count_label = font.render("Count", True, (255, 255, 255))
            self.screen.blit(true_count_label, (x + 10, y + 10))

    def draw_true_count(self):
        # Define the coordinates and dimensions of the box
        x, y = 975, 175
        width, height = 200, 50

        # Create a rect for the box
        true_count_rect = pygame.Rect(x, y, width, height)

        # Check if the mouse is hovering over the box
        if true_count_rect.collidepoint(pygame.mouse.get_pos()):
            # Draw the box with a light blue color
            pygame.draw.rect(self.screen, (173, 216, 230), true_count_rect)

            # Render and display the true count text
            font = pygame.font.Font(None, 24)
            true_count_text = font.render(
                f"True Count: {self.true_count}", True, (0, 0, 0)
            )
            self.screen.blit(true_count_text, (x + 10, y + 10))
        else:
            # Draw the box with a dark blue color
            pygame.draw.rect(self.screen, (0, 0, 128), true_count_rect)

            # Render and display the label "True Count"
            font = pygame.font.Font(None, 24)
            true_count_label = font.render("True Count", True, (255, 255, 255))
            self.screen.blit(true_count_label, (x + 10, y + 10))

    def draw_bet_slider(self):
        # Coordinates
        slider_x, slider_y = 350, 325
        slider_width, slider_height = 300, 20

        # Draw the slider track
        slider_track_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        pygame.draw.rect(self.screen, (128, 128, 128), slider_track_rect)

        # Calculate the position of the slider button based on the current bet size
        max_bet = 500
        min_bet = 10
        slider_button_x = slider_x + (slider_width - 10) * (
            self.players[0].bet_size - min_bet
        ) / (max_bet - min_bet)
        slider_button_y = slider_y - 5

        # Draw the slider button
        self.slider_button_rect = pygame.Rect(slider_button_x, slider_button_y, 20, 30)
        pygame.draw.rect(self.screen, (0, 0, 128), self.slider_button_rect)

        # Render and display the current bet size text
        font = pygame.font.Font(None, 24)
        bet_text = font.render(
            f"Bet: {self.players[0].bet_size}", True, (255, 255, 255)
        )
        self.screen.blit(bet_text, (slider_x, slider_y - 25))

    def check_bet_slider(self, event):
        # Coordinates
        slider_x, slider_y = 350, 325
        slider_width, slider_height = 300, 20

        max_bet = 500
        min_bet = 10

        # Check for mouse events to update the bet size when the slider is moved
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_button_rect.collidepoint(event.pos):
                self.dragging_slider = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_slider = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider:
                # Calculate the new bet size based on the slider position
                slider_button_x = max(
                    slider_x, min(slider_x + slider_width - 10, event.pos[0])
                )
                bet_range = max_bet - min_bet
                self.players[0].bet_size = (
                    round(
                        (slider_button_x - slider_x) / (slider_width - 10) * bet_range
                    )
                    + min_bet
                )