"""
Interactive single-player Blackjack game.
Designed to use object-oriented programming in Python 3.7.3
"""
from random import shuffle


class Card:
    """Card class to store rank, value and function
    to switch from Ace-High to Ace-Low
    """
    def __init__(self, rank):
        self.rank = rank
        self.ace_high = False

        if (rank == 'J') or (rank == 'Q') or (rank == 'K'):
            self.value = 10
        elif rank == 'A':
            self.value = 11
            self.ace_high = True
        else:
            try:
                self.value = int(rank)
            except Exception:
                print("Bad card rank! Unable to determine value")

    def AceLow(self):
        """Function to switch from Ace-High to Ace-Low"""
        if self.rank == 'A':
            self.value = 1
            self.ace_high = False

    def GetOpeningValue(self):
        """Function to return value of first dealer card as 11
        when dealt a pair of aces
        """
        if self.rank == 'A':
            return 11
        else:
            return self.value


class Deck:
    """Deck class to initialise and shuffle a given number of packs"""
    def __init__(self, number_of_packs):
        self.cards = [Card(card) for card in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                       'J', 'Q', 'K', 'A'] * 4 * number_of_packs]
        shuffle(self.cards)

    def DealCards(self, number_of_cards):
        """Function to deal a given number of cards"""
        cards = []
        for i in range(number_of_cards):
            cards.append(self.cards.pop())
        return cards


class Hand:
    """Hand class to store list of Card objects and functions
    to draw cards and calculate hand value
    """
    def __init__(self):
        self.cards = deck.DealCards(2)
        self.value = self.GetValue()

    def GetValue(self):
        """Function to calculate value of hand"""
        total = 0
        aces_high = []

        for card in self.cards:
            total = total + card.value
            if card.ace_high:
                aces_high.append(card)

        if (total > 21) and (len(aces_high) > 0):
            aces_high[0].AceLow()
            return self.GetValue()
        elif (total < 3) or (type(total) != int):
            raise ValueError("Unable to get value of cards.")
        else:
            return total

    def DrawCards(self, cards_to_draw):
        """Function to draw more cards from Deck object"""
        self.cards.extend(deck.DealCards(cards_to_draw))
        self.value = self.GetValue()

    def Blackjack(self):
        """Function to determine if hand has Blackjack"""
        if self.value == 21:
            return True
        else:
            return False

    def Bust(self):
        """Function to determine if hand is Bust"""
        if self.value > 21:
            return True
        else:
            return False

    def Soft(self):
        """Function to determine if hand is Soft"""
        if self.value < 17:
            return True
        else:
            return False


def PlayerOut():
    """Function to see if player has Blackjack or Bust"""
    if player_hand.Blackjack():
        print("\nBlackjack! You win!")
        return True
    elif player_hand.Bust():
        print("\nBust! You lose!")
        return True
    else:
        return False


def DealerOut():
    """Function to see if dealer has Blackjack, Bust or Soft"""
    if dealer_hand.Blackjack():
        print("\nBlackjack! You lose!")
        return True
    elif dealer_hand.Bust():
        print("\nThe dealer busts! You win!")
        return True
    else:
        return False


def DealerLogic():
    """Function to handle dealer decision making
    once player decides to 'Stand/Stick'
    """
    print("\nThe dealer's hand is:\n{} with a value of {}".format(
            [card.rank for card in dealer_hand.cards], dealer_hand.value))
    print("\nYour hand is:\n{} with a value of {}".format(
            [card.rank for card in player_hand.cards], player_hand.value))

    if not DealerOut():
        if (dealer_hand.Soft()):
            print("\nThe dealer hits!")
            dealer_hand.DrawCards(1)
            DealerLogic()
        elif dealer_hand.value == player_hand.value:
            print("\nThe dealer stands! Draw!")
        elif dealer_hand.value < player_hand.value:
            print("\nThe dealer stands! You win!")
        else:
            print("\nThe dealer stands! You lose!")


def StandorHit():
    """Function to deal with player decision to stand/hit after initial deal"""
    print("\nThe dealer shows they have a:\n{} with a value of {}".format(
            [dealer_hand.cards[0].rank],
            dealer_hand.cards[0].GetOpeningValue()))
    print("\nYour hand is:\n{} with a value of {}".format(
            [card.rank for card in player_hand.cards], player_hand.value))

    if not PlayerOut():
        try:
            decision = int(input("\nWhat would you like do?\n"
                                 "1. Stand/Stick\n2. Hit/Twist\n"
                                 "3. Quit Game\n"))

            if decision == 1:
                DealerLogic()
            elif decision == 2:
                print("\nThe player hits!")
                player_hand.DrawCards(1)
                StandorHit()
            elif decision == 3:
                print("\nGoodbye!")
            else:
                BadInput(StandorHit, 'Stand/Stick', 'Hit/Twist', 'Quit Game')

        except Exception:
            BadInput(StandorHit, 'Stand/Stick', 'Hit/Twist', 'Quit Game')


def BadInput(func, *args):
    """Function to return user to input menu if an error occurs"""
    message = "\nOops! There seems to be a problem.\n"
    if len(args) < 1:
        message = message + "Input error. Please try again."
    else:
        for ar in args:
            if args.index(ar) == 0:
                message = message + "Please enter {} for '{}'".format(1, ar)
            else:
                message = message + \
                          " or {} for '{}'".format(args.index(ar) + 1, ar)
        message = message + "."
    print(message)
    func()


def PlayBlackjack():
    """Game engine function"""
    try:
        play = int(input("Would you like to play Blackjack?\n"
                         "1. Yes\n2. No\n"))

        if play == 1:
            print("\nLet's play Blackjack!")
            StandorHit()

        elif play == 2:
            print("\nGoodbye!")

        else:
            BadInput(PlayBlackjack, 'Yes', 'No')

    except Exception:
        BadInput(PlayBlackjack, 'Yes', 'No')


if __name__ == '__main__':
    """Deck and player/dealer hands set as global variables"""
    deck = Deck(1)
    player_hand = Hand()
    dealer_hand = Hand()

    PlayBlackjack()
