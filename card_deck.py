import math
import random
from typing import List

class Card:
    
    def __init__(self, face, suit, value) -> None:
        self.is_visible = False
        self.face = face # Not really needed but want to store
        self.suit = suit
        self.value = value
    
    def flip(self):
        self.is_visible = not self.is_visible


class CardDeck:

    def __init__(self) -> None:
        self.deck: List[Card] = []
        card_types = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        card_suits = ['\u2660', '\u2665', '\u2663', '\u2666',]
        # Standard Bicycle Playing Cards order:
        # A through K of Spades
        i = 1
        for type in card_types:
            self.deck.append(Card(type + card_suits[0], card_suits[0], min(i, 10)))
            i += 1
        # A through K of Diamonds
        i = 1
        for type in card_types:
            self.deck.append(Card(type + card_suits[1], card_suits[1], min(i, 10)))
            i += 1
        # K through A of Clubs
        i = len(card_types)
        for type in reversed(card_types):
            self.deck.append(Card(type + card_suits[2], card_suits[2], min(i, 10)))
            i -= 1
        #  K through A of Hearts
        i = len(card_types)
        for type in reversed(card_types):
            self.deck.append(Card(type + card_suits[3], card_suits[3], min(i, 10)))
            i -= 1
    
    def take_card(self):
        return self.deck.pop(0)

    def print_deck(self):
        # Print out the deck of cards
        for card in self.deck:
            print(card.face, end=' ')
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
            print(card.face, end=' ')
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