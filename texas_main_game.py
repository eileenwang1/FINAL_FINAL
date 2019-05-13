
from texas_value import shuffle
from texas_value import value_seven as valueCards
import random

S_ALLIN = 'allin'
FOLD = 'fold'

class Players():

    def __init__(self, name = None):
        self.chips = 100
        self.name = name

    def win(self, pot_size):
        self.chips += pot_size
        print("{} win {}, and your money now is {}".format(self.name, pot_size, self.chips))

    def all_in(self):
        return self.chips == 0

    def broke(self):
        return self.chips == 0

    def bet(self, other, pot, your_size = 0, other_size = 0, other_all_in = False):  ### not for fold###
        #####------------------------------------------------------------########
        #       change to try-except, replace input/output by functions         #
        #####------------------------------------------------------------########
        if other_all_in:
            to_call = other_size - your_size
            if to_call > self.chips:
                to_call = self.chips
            status = '{} goes all-in. Do you want to call or fold?'.format(other.name)
            instructions = '''enter 0 for fold, {0} for call'''.format(to_call)
            bet_size = int(input('{} {}'.format(status, instructions)))
            return bet_size

        if other_size - your_size > 0:
            to_call = other_size - your_size
            to_raise = other_size + to_call
            if to_raise >= self.chips:
                to_raise = self.chips
            all_in = self.chips

            status = 'Do you want to call, raise, or fold?'
            instructions = '''enter 0 for fold, {0} for call, {1} for all-in or anything between {2} and {1} for raise '''\
                .format(to_call, all_in, to_raise)

            if all_in < to_call:
                status = 'Do you want to call (all-in), or fold?'
                instructions = '''enter 0 for fold, or {} for all-in'''.format(all_in)
                bet_size = int(input("{} bets {}, {}, {}".format(other.name, other_size, status, instructions)))
                if bet_size != 0 and bet_size != all_in:
                    print("Warning, you can only call or all-in now. Wrong input again will be treated as a Fold".format(to_call))
                    bet_size = int(input("{} bets {}, {}, {}".format(other.name, other_size, status, instructions)))

            else:
                bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
                if 0 < bet_size < to_call:
                    print("Warning, you need to bet at least {} to call. Wrong input again will be treated as a Fold".format(to_call))
                    bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
                elif to_call < bet_size < to_raise:
                    print("Warning, you need to bet at least {} to raise. Wrong input again will be treated as a Fold".format(to_raise))
                    bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
                elif self.chips < bet_size:
                    print("Warning, you have only {} chips left. Wrong input again will be treated as a Fold".format(self.chips))
                    bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status,instructions)))

            if bet_size == 0:
                return FOLD

        else:
            all_in = self.chips
            status = 'Do you want to check or bet?'
            instructions = '''enter 0 for check, or no more than {} for bet '''.format(all_in)
            bet_size = int(input('{} {}'.format(status, instructions)))
        self.chip_change(bet_size, pot)
        return bet_size

    def chip_change(self, bet_size, pot):
        self.chips -= bet_size
        pot.size += bet_size
        return bet_size

    def __repr__(self):
        return str(self.chips)

class Pot():
    def __init__(self):
        self.size = 0

    def bets(self, bet):
        self.size += bet

    def reset(self):
        self.size = 0

    def __repr__(self):
        return str(self.size)


pot = Pot()
player1 = Players("Alice")
player2 = Players("Bob")







def actions(first, second, round, pot, sb = 1, bb = 2):
    if first.all_in() or second.all_in():
        return 0

    if round == 0:
        size1 = sb
        size2 = bb
        first.chip_change(sb, pot)
        second.chip_change(bb, pot)

    else:
        size1, size2 = 0,0

    current = first.bet(second, pot, size1, size2)
    if current == FOLD:
        player2.win(pot.size)
        return FOLD
    size1 += current
    # bet(self, other, pot, my_size = 0, other_size = 0):

    current = second.bet(first, pot, size2, size1)
    if current == FOLD:
        player1.win(pot.size)
        return FOLD
    size2 += current

    while not size1 == size2:

        current = first.bet(second, pot, size1, size2)
        if current == FOLD:
            player2.win(pot.size)
            return FOLD
        size1 += current
        # bet(self, other, pot, my_size = 0, other_size = 0):
        if size1 == size2:
            break

        current = second.bet(first, pot, size2, size1)
        if current == FOLD:
            player1.win(pot.size)
            return FOLD
        size2 += current


def game(player1, player2, pot):
    pot.reset()

    deck = shuffle()
    random.shuffle(deck)

    print("player 1 gets",deck[0],deck[1],"\t\t\tplayer 2 gets",deck[7],deck[8])
    result = actions(player2, player1, 0, pot)
    if result == FOLD:
        return

    print(deck[2],deck[3],deck[4],"\t\t\t\t",deck[2],deck[3],deck[4])
    actions(player1, player2, 1, pot)
    if result == FOLD:
        return

    print(deck[5],"\t\t\t\t\t",deck[5])
    actions(player1, player2, 2, pot)
    if result == FOLD:
        return

    print(deck[6],"\t\t\t\t\t",deck[6])
    actions(player1, player2, 3, pot)
    if result == FOLD:
        return


    v1=valueCards(deck[0:7])
    print("for player 1, ",v1)
    v2=valueCards(deck[2:9])
    print("for player 2, ",v2)

    if v1>v2:
        print("player 1 wins!")
        player1.win(pot.size)

    elif v1<v2:
        print("player 2 wins!")
        player2.win(pot.size)

    else:
        print("it is a draw.")
        player1.win(pot.size//2)
        player2.win(pot.size//2)

    pot.reset()
game(player1, player2, pot)