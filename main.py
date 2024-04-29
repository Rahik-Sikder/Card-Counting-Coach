from card_deck import *

def main():
    # card_deck = CardDeck()
    # card_deck.print_deck()
    # card_deck.shuffle_deck()
    # card_deck.print_deck()
    new_shoe = Shoe(4)
    new_shoe.print_shoe()
    print()
    new_shoe.reset_shoe(6)
    new_shoe.print_shoe()

    pass


if __name__ == '__main__':
    main()