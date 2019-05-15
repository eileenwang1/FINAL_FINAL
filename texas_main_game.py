


"""
Created on Tue Jul 22 00:47:05 2014
@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import threading
import random

S_ALLIN = 'allin'
FOLD = 'fold'

#### change
from texas_value import shuffle
from texas_value import value_seven as valueCards


class Players():
    def __init__(self, name=None, client=None):
        self.client = client
        self.chips = 100
        self.name = name
        self.status = ''
        self.instructions = ''
        self.to_send = ''
        self.to_recieve = []
        self.action = ''


    def win(self, pot_size):
        self.chips += pot_size
        self.out_put("Congratulations! you win {}, and your money now is {}".format(pot_size // 2, self.chips))
    def lose(self, pot_size):
        self.out_put("you lose {} during the hand. Your money now is {}".format(pot_size // 2, self.chips))
    def split(self, pot_size):
        self.chips += pot_size // 2
        self.out_put("You split the money. Your money now is {}".format(self.chips))
    def all_in(self):
        return self.chips == 0
    def broke(self):
        return self.chips == 0
    def bet(self, other, pot, your_size=0, other_size=0, other_all_in=False):  ### not for fold###
        #####------------------------------------------------------------########
        #       change to try-except, replace input/output by functions         #
        #####------------------------------------------------------------########
        if other_all_in:
            to_call = other_size - your_size
            if to_call > self.chips:
                to_call = self.chips
            self.status = '{} goes all-in. Do you want to call or fold? The pot is now {}.'.format(other.name, pot.size)
            self.instructions = '''Enter 0 for fold, {0} for call'''.format(to_call)
            bet_size = self.get_bet_size()
            return bet_size
        if other_size - your_size > 0:
            to_call = other_size - your_size
            to_raise = other_size + to_call
            if to_raise >= self.chips:
                to_raise = self.chips
            all_in = self.chips
            self.status = '{} bets {} in total. Do you want to call, raise, or fold? The pot is now {}.'.format(
                other.name, other_size, pot.size)
            self.instructions = '''Enter 0 for fold, {0} for call, {1} for all-in or anything between {2} and {1} for raise ''' \
                .format(to_call, all_in, to_raise)
            if all_in < to_call:
                self.status = 'Do you want to call (all-in), or fold? The pot is now {}.'.format(pot.size)
                self.instructions = '''Enter 0 for fold, or {} for all-in'''.format(all_in)
                bet_size = self.get_bet_size()
                if bet_size != 0 and bet_size != all_in:
                    self.out_put(
                        "Warning, you can only call or all-in now. Wrong input again will be treated as a Fold".format(
                            to_call))
                    bet_size = self.get_bet_size()
            else:
                bet_size = self.get_bet_size()
                if 0 < bet_size < to_call:
                    self.out_put(
                        "Warning, you need to bet at least {} to call. Wrong input again will be treated as a Fold".format(
                            to_call))
                    bet_size = self.get_bet_size()
                elif to_call < bet_size < to_raise:
                    self.out_put(
                        "Warning, you need to bet at least {} to raise. Wrong input again will be treated as a Fold".format(
                            to_raise))
                    bet_size = self.get_bet_size()
                elif self.chips < bet_size:
                    self.out_put(
                        "Warning, you have only {} chips left. Wrong input again will be treated as a Fold".format(
                            self.chips))
                    bet_size = self.get_bet_size()

            if bet_size == 0:
                return FOLD
        else:
            all_in = self.chips
            self.status = 'Do you want to check or bet? The pot is now {}.'.format(pot.size)
            self.instructions = '''Enter 0 for check, or no more than {} for bet '''.format(all_in)
            bet_size = self.get_bet_size()
        self.chip_change(bet_size, pot)
        return bet_size
    def chip_change(self, bet_size, pot):
        self.chips -= bet_size
        pot.size += bet_size
        return bet_size

    def __repr__(self):
        return str(self.chips)



    def out_put(self, message):
        self.to_recieve.append(message)
        print('[ {} ]'.format(self.name), message)
        return
        mysend(to_sock, json.dumps({"action": "exchange_g", "from": msg["from"], "message": msg["message"]}))



    def input_instructions(self, message):
        self.out_put(message)
        user_input = None
        while len(self.action) == 0:
            time.sleep(CHAT_WAIT)


        if len(self.action) > 0:
            user_input = self.action

            try:
                user_input = int(user_input)

            except:
                self.out_put('You have to enter an integer. Invalid input again would be treated as a Fold')
                user_input = self.input_instructions(message)
                try:
                    user_input = int(user_input)
                except:
                    user_input = 0

        if not user_input is None:
            self.action = ''
            return user_input

    def get_bet_size(self):
        message = '{} \n{}'.format(self.status, self.instructions)
        return self.input_instructions(message)


class Pot():
    def __init__(self):
        self.size = 0
    def bets(self, bet):
        self.size += bet
    def reset(self):
        self.size = 0
    def __repr__(self):
        return str(self.size)


def actions(first, second, round, pot, sb=1, bb=2):
    if first.all_in() or second.all_in():
        return 0
    if round == 0:
        size1 = sb
        size2 = bb
        first.chip_change(sb, pot)
        second.chip_change(bb, pot)
    else:
        size1, size2 = 0, 0
    current = first.bet(second, pot, size1, size2)
    if current == FOLD:
        second.win(pot.size)
        return FOLD
    size1 += current
    # bet(self, other, pot, my_size = 0, other_size = 0):

    current = second.bet(first, pot, size2, size1)
    if current == FOLD:
        first.win(pot.size)
        return FOLD
    size2 += current
    while not size1 == size2:
        current = first.bet(second, pot, size1, size2)
        if current == FOLD:
            second.win(pot.size)
            return FOLD
        size1 += current
        # bet(self, other, pot, my_size = 0, other_size = 0):
        if size1 == size2:
            break
        current = second.bet(first, pot, size2, size1)
        if current == FOLD:
            first.win(pot.size)
            return FOLD
        size2 += current


def game(player1, player2, pot):
    pot.reset()
    deck = shuffle()
    random.shuffle(deck)
    player1_card = 'Your hand: {} {}'.format(deck[0], deck[1])
    player2_card = 'Your hand: {} {}'.format(deck[7], deck[8])
    player1.out_put(player1_card)
    player2.out_put(player2_card)
    result = actions(player2, player1, 0, pot)
    if result == FOLD:
        return
    common_msg = 'Communal cards: {} {} {}'.format(deck[2], deck[3], deck[4])
    player1_msg = '{} {}'.format(common_msg, player1_card)
    player2_msg = '{} {}'.format(common_msg, player2_card)
    player1.out_put(player1_msg)
    player2.out_put(player2_msg)
    actions(player1, player2, 1, pot)
    if result == FOLD:
        return
    common_msg = 'Communal cards: {} {} {} {} '.format(deck[2], deck[3], deck[4], deck[5])
    player1_msg = '{} {}'.format(common_msg, player1_card)
    player2_msg = '{} {}'.format(common_msg, player2_card)
    player1.out_put(player1_msg)
    player2.out_put(player2_msg)
    actions(player1, player2, 2, pot)
    if result == FOLD:
        return
    common_msg = 'Communal cards: {} {} {} {} {} '.format(deck[2], deck[3], deck[4], deck[5], deck[6])
    player1_msg = '{} {}'.format(common_msg, player1_card)
    player2_msg = '{} {}'.format(common_msg, player2_card)
    player1.out_put(player1_msg)
    player2.out_put(player2_msg)
    actions(player1, player2, 3, pot)
    if result == FOLD:
        return
    v1 = valueCards(deck[0:7])
    v2 = valueCards(deck[2:9])
    player1_msg = 'You got {}. {} got {}'.format(v1[2], player2.name, v2[2])
    player2_msg = 'You got {}. {} got {}'.format(v2[2], player1.name, v1[2])
    player1.out_put(player1_msg)
    player2.out_put(player2_msg)
    if v1 > v2:
        player1.win(pot.size)
        player2.lose(pot.size)
    elif v1 < v2:
        player2.win(pot.size)
        player1.lose(pot.size)
    else:
        player1.split(pot.size)
        player2.split(pot.size)
    pot.reset()


def game_start(game_player1, game_player2):
    pot = Pot()
    game(game_player1, game_player2, pot)







