import math
import random
from typing import List

rank_map = {
    'A': '01',
    '2': '02',
    '3': '03',
    '4': '04',
    '5': '05',
    '6': '06',
    '7': '07',
    '8': '08',
    '9': '09',
    '10': '10',
    'J': 'C1J',
    'Q': 'C2Q',
    'K': 'C3K',
    '\u2660' : 'S', 
    '\u2665' : 'D', 
    '\u2663' : 'C', 
    '\u2666': 'H'
}

class Card:
    
    def __init__(self, rank, suit, value, is_visible=True) -> None:
        self.is_visible = False
        self.rank = rank
        self.suit = suit
        self.value = value
        self.png = ''
        self.__set_visible()
        
    def __set_visible(self):
        if not self.is_visible:
            self.png = './card_jpgs/card_back.jpeg'
        else:
            self.png = f'./card_jpgs/{rank_map[self.suit]}{rank_map[self.rank]}.jpg'
    
    def flip(self):
        self.is_visible = not self.is_visible
        self.__set_visible()
    
    def __str__(self) -> str:
        return self.rank + self.suit


class CardDeck:

    def __init__(self) -> None:
        self.deck: List[Card] = []
        card_types = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        card_suits = ['\u2660', '\u2665', '\u2663', '\u2666',]
        # Standard Bicycle Playing Cards order:
        # A through K of Spades
        i = 1
        for type in card_types:
            self.deck.append(Card(type, card_suits[0], min(i, 10)))
            i += 1
        # A through K of Diamonds
        i = 1
        for type in card_types:
            self.deck.append(Card(type, card_suits[1], min(i, 10)))
            i += 1
        # K through A of Clubs
        i = len(card_types)
        for type in reversed(card_types):
            self.deck.append(Card(type, card_suits[2], min(i, 10)))
            i -= 1
        #  K through A of Hearts
        i = len(card_types)
        for type in reversed(card_types):
            self.deck.append(Card(type, card_suits[3], min(i, 10)))
            i -= 1
    
    def take_card(self):
        return self.deck.pop(0)

    def print_deck(self):
        # Print out the deck of cards
        for card in self.deck:
            print(card, end=' ')
        print()

    def shuffle_deck(self):
        # Shuffle the deck of cards
        random.shuffle(self.deck)



class Shoe:

    def __init__(self, shoe_size) -> None:
        # All decks in a shoe are shuffled at once
        self.cards: List[Card] = []
        self.decks_in_shoe = shoe_size
        for i in range(shoe_size):
            new_deck = CardDeck()
            for j in range(52):
                self.cards.append(new_deck.take_card())
        random.shuffle(self.cards)
    
    def print_shoe(self):
        # Print out the deck of cards
        for card in self.cards:
            print(card, end=' ')
        print()

    def reset_shoe(self, shoe_size) -> None:
        self.cards: List[Card] = []
        self.decks_in_shoe = shoe_size
        for i in range(shoe_size):
            new_deck = CardDeck()
            for j in range(52):
                self.cards.append(new_deck.take_card())
        random.shuffle(self.cards)

    def take_card(self):
        return self.cards.pop(0)
    
    def length(self):
        return len(self.cards)