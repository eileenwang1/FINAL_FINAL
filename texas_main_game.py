
from value import cards
from value import value_seven as valueCards
import random

class Players():

    def __init__(self, name):
        self.chips = 100
        self.name = name

    def win(self, pot_size):
        self.chips += pot_size

    def bet(self, other, pot, my_size = 0, other_size = 0):
        if other_size > 0:
            to_call = other_size - your_size
            to_raise = other_size + to_call
            status = 'Do you want to call, raise, or fold?'
            instructions = '''enter 0 for fold, {} or for call, {} for all-in or anything higher than {} for raise'''\
                .format(to_call, to_raise, self.chips)

            bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
            if bet_size < to_call and self._chips >= to_call:
                print("Warning, you need to bet at least {} to call. Wrong input again will be treated as a Fold".format(to_call))
                bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
            elif to_call < bet_size < to_raise and self.chips >= to_raise:
                print("Warning, you need to bet at least {} to raise. Wrong input again will be treated as a Fold".format(to_raise))
                bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status, instructions)))
            elif self.chips < bet_size:
                print("Warning, you have only {} chips left. Wrong input again will be treated as a Fold".format(self.chips))
                bet_size = int(input("{} bets {}, you need {} to call. {} {}".format(other.name, other_size, to_call, status,instructions)))

        self.chips -= bet_size
        pot.chips += bet_size
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
player1 = Players()
player2 = Players()

deck=cards()
random.shuffle(deck)

print("player 1 gets",deck[0],deck[1],"\t\t\tplayer 2 gets",deck[7],deck[8])
betting(player1, player2, 0)

print(deck[2],deck[3],deck[4],"\t\t\t\t",deck[2],deck[3],deck[4])
betting(player1, player2, 1)

print(deck[5],"\t\t\t\t\t",deck[5])
betting(player1, player2, 2)

print(deck[6],"\t\t\t\t\t",deck[6])
betting(player1, player2, 3)



def actions(first, second, round, sb = 1, bb = 2):
    first.bet(sb)
    second.bet(bb)
    size1 = first.bet()
    size2 = second.bet()



v1=valueCards(deck[0:7])
print("for player 1, ",v1)
v2=valueCards(deck[2:9])
print("for player 2, ",v2)

if v1>v2:
    print("player 1 wins!")
    player1.win(pot.size)
    pot.reset()
elif v1<v2:
    print("player 2 wins!")
    player2.win(pot.size)
    pot.reset()

else:
    print("it is a draw.")
    player1.win(pot.size//2)
    player2.win(pot.size//2)
    pot.reset()

