from itertools import permutations
from itertools import product
import numpy as np

class GameModel:

    def __init__(self):
        self.colours = ['red', 'green', 'blue']
        self.types = ['1', '2', '3']
        deck = list(product(self.types, self.colours))
        shuffled_deck = np.random.permutation(deck)

        self.players_number = 3
        self.cards = list()
        number_for_player = (len(shuffled_deck)-1) // self.players_number

        for i in range(self.players_number):
            self.cards.append(shuffled_deck[i*number_for_player: (i+1)*number_for_player])

        self.cards_hiden = shuffled_deck[number_for_player*self.players_number:number_for_player*self.players_number+1]
        self.cards_open =shuffled_deck[number_for_player*self.players_number+1:]

x = GameModel()
print(x.cards)
print(x.cards_open)
print(x.cards_hiden)