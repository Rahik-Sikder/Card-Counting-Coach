from card_deck import *
from typing import List
import math
import pygame
from pygame.locals import *

CARD_SIZE = 115

class Player:

    def __init__(
        self, name, screen, position, stack=500, is_bot=True, bot_level=0
    ) -> None:
        # Drawing
        self.screen = screen
        self.position: tuple = position
        # Game Info
        self.name = name
        self.is_bot = is_bot
        self.bot_level = bot_level
        self.current_cards: List[Card] = []
        self.value = 0
        self.stack = stack
        # Will add functionality for this later
        self.bet_size = 25

    def make_guess(self) -> str:
        if self.bot_level > 0:
            return "Hit" if self.value < 17 or random.randint(1, 10) < 2 else "Stand"
        else:
            return random.choice(["Hit", "Stand"])

    def take_card(
        self,
        card: Card,
    ) -> None:
        self.value += card.value
        self.current_cards.append(card)

    def clear_hand(self) -> None:
        self.current_cards: List[Card] = []

    def draw_player(self) -> None:
        offset = 0
        name_font = pygame.font.Font(None, 24)
        name_tag = name_font.render(self.name, True, (255, 255, 255))
        self.screen.blit(name_tag, (self.position[0], self.position[1]))

        for card in self.current_cards:
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
                (self.position[0] + offset, self.position[1] + 20 + offset / 2),
            )
            offset += 30


class BlackJack:

    def __init__(self, screen, shoe_size=4, num_bots=0) -> None:
        # Drawing
        self.screen = screen
        # Game Info
        num_bots = min(6, num_bots)  # Max of 7 players
        self.num_players = 1 + num_bots
        self.shoe = Shoe(shoe_size)
        self.running_count = 0
        self.true_count = 0
        self.true_true_count = 0  # Accounts for burn cards
        self.is_player_turn = True
        self.dealer = Player("Dealer", screen, (800, 100), is_bot=False)
        self.players: List[Player] = [Player("You", screen, (75, 300), is_bot=False)]
        for i in range(min(6, num_bots)):
            self.players.append(
                Player(
                    f"Bot {i+1}",
                    screen,
                    (((1000 / num_bots) + i * (1400 / num_bots)), 600),
                    bot_level=i,
                )
            )

    def new_round_start(self):
        self.deal_card(self.dealer, face_up=False)
        self.deal_card(self.dealer)
        for player in self.players:
            player.clear_hand()
            self.deal_card(player)
            self.deal_card(player)

    def play_round(self, action: str) -> str:
        """
        If it's the player's turn they can choose to Hit or Stand.
        TODO: Functionality for Splitting
        """
        if not self.is_player_turn:
            return "Not Your Turn"

        elif action == "Stand":
            self.is_player_turn = False
            return "Stood"

        elif action == "Hit":
            self.deal_card(self.players[0])

    def bots_play_round(self) -> None:
        for i in range(1, len(self.num_players)):
            cur_bot: Player = self.players[i]
            while cur_bot.make_guess() == "Hit" and cur_bot.value < 21:
                self.deal_card(cur_bot)

    def evaluate_round(self) -> str:
        for player in self.players:
            if player.value > 21 or player.value < self.dealer.value:
                player.stack -= player.bet_size
            elif player.value > self.dealer.value:
                player.stack += player.bet_size

    def draw_players(self) -> None:
        self.dealer.draw_player()
        for player in self.players:
            # print("Drawing player ", player.name, " at position ", player.position)
            player.draw_player()

    def deal_card(self, player: Player, face_up=True):
        card = self.shoe.take_card()
        if face_up:
            card.flip()
        player.take_card(card)
