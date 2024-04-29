from card_deck import *
from typing import List

class Player:

    def __init__(self, name, stack=500, is_bot=True, bot_level=0) -> None:
        self.name  = name
        self.is_bot = is_bot
        self.bot_level = bot_level
        self.current_cards: List[Card] = []
        self.value = 0
        self.stack = stack
        # Will add functionality for this later
        self.bet_size = 25
    
    def make_guess(self) -> str:
        if self.bot_level > 0:
            return 'Hit' if self.value < 17 or random.randint(1, 10) < 2 else 'Stand'
        else:
            return random.choice(['Hit', 'Stand'])
    
    def take_card(self, card:Card,) -> None:
        self.value += card.value
        self.current_cards.append(card)
    
    def clear_hand(self) -> None:
        self.current_cards: List[Card] = []    


class BlackJack:

    def __init__(self, shoe_size=4, num_bots=0) -> None:
        self.num_players = 1
        self.shoe = Shoe(shoe_size)
        self.running_count = 0
        self.true_count = 0
        self.true_true_count = 0 # Accounts for burn cards 
        self.is_player_turn = True
        self.dealer = Player("Dealer", is_bot=False)
        self.players: List[Player] = {Player("You", is_bot=False)}
        for i in range(1, num_bots + 1):
            self.players.append(Player("Bot " + i, bot_level=i))    

    def new_round_start(self):
        self.deal_card(self.dealer)
        self.deal_card(self.dealer, face_up=False)
        for player in self.players:
            player.clear_hand()
            self.deal_card(player)
            self.deal_card(player)

    def play_round(self, action: str) -> str:
        '''
        If it's the player's turn they can choose to Hit or Stand.
        TODO: Functionality for Splitting
        '''
        if not self.is_player_turn: 
            return 'Not Your Turn'
        
        elif action == 'Stand':
            self.is_player_turn = False
            return 'Stood'

        elif action == 'Hit':
            self.deal_card(self.players[0]) 

    def bots_play_round(self) -> None:
        for i in range(1, len(self.num_players)):
            cur_bot: Player = self.players[i]
            while cur_bot.make_guess() == 'Hit' and cur_bot.value < 21:
                self.deal_card(cur_bot)

    def evaluate_round(self) -> str:
        for player in self.players:
            if player.value > 21 or player.value < self.dealer.value:
                player.stack -= player.bet_size
            elif player.value > self.dealer.value:
                player.stack += player.bet_size

    def deal_card(self, player: Player, face_up=True):
        card = self.shoe.take_card()
        if face_up:
            card.flip()
        player.take_card(card)




    