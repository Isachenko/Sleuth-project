from itertools import permutations
from itertools import product
import numpy as np
from enum import Enum


class GameState(Enum):
    QUESTION_CHOOSING = 1
    PLAYER_TO_ASK_CHOOSING = 2


class GameModel:

    def __init__(self):
        self.game_state = GameState.QUESTION_CHOOSING

        self.colours = ['red', 'green', 'blue']
        self.types = ['1', '2', '3']
        deck = list(product(self.types, self.colours))
        shuffled_deck = np.random.permutation(deck)

        self.players_number = 3
        self.questions_in_hand_number = 3
        self.cards = list()
        number_for_player = (len(shuffled_deck)-1) // self.players_number

        self.players_names = ["player {}".format(i+1) for i in range(self.players_number)]

        for i in range(self.players_number):
            self.cards.append(shuffled_deck[i*number_for_player: (i+1)*number_for_player])

        self.cards_hidden = shuffled_deck[number_for_player*self.players_number:number_for_player*self.players_number+1]
        self.cards_open =shuffled_deck[number_for_player*self.players_number+1:]

        self.questions_deck = list(product(["number_of"], self.types)) + list(product(["number_of"], self.colours))
        self.questions_deck += deck
        self.questions_deck_shuffled = np.random.permutation(self.questions_deck)

        self.question_index = 0
        self.players_questions = []
        for i in range(self.players_number):
            questions = [self.next_question_card() for _ in range(self.questions_in_hand_number)]
            self.players_questions.append(questions)

        self.current_turn_player = 0

    def next_question_card(self):
        question_card = self.questions_deck_shuffled[self.question_index]
        self.question_index += 1
        if self.question_index >= len(self.questions_deck_shuffled):
            self.questions_deck_shuffled = np.random.permutation(self.questions_deck)
            self.question_index = 0
        return question_card

    def get_cuurent_player_questions(self):
        return self.players_questions[self.current_turn_player]

    def next_turn(self):
        self.current_turn_player += 1
        self.current_turn_player %= self.players_number

    def question_chosen(self, question):

        if (self.game_state == GameState.QUESTION_CHOOSING):
            #ask it
            self.question_gonna_ask = question

            #remove question
            for i in range(self.questions_in_hand_number):
                if (self.players_questions[self.current_turn_player][i][0] == question[0]) and \
                    (self.players_questions[self.current_turn_player][i][1] == question[1]):
                    del self.players_questions[self.current_turn_player][i]
                    break

            #add new one
            self.players_questions[self.current_turn_player].append(self.next_question_card())

            self.game_state = GameState.PLAYER_TO_ASK_CHOOSING

    def player_to_ask_choosen(self, player):
        if self.game_state == GameState.PLAYER_TO_ASK_CHOOSING:
            print(self.question_gonna_ask)
            print(player)

            self.game_state = GameState.QUESTION_CHOOSING
            self.next_turn()



    def updateModel(self):
        pass




if __name__ == "__main__":

    x = GameModel()

    print("players_questions")
    print(x.players_questions)
