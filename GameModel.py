from itertools import permutations
from itertools import product
import numpy as np
from enum import Enum
from KripkeModel import KripkeModel

countable = {1: "1-st", 2: "2-nd", 3: "3-rd"}
has_or_not = {True: "has", False: "hasn't"}

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

        self.kripke = KripkeModel(self.players_number, deck, self.cards_open)

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
            #print(player + ", " + self.question_gonna_ask + "?")
            pl_n = int(player[-1:])

            if self.question_gonna_ask[0] == "number_of":
                self.ask_number_of(pl_n, self.question_gonna_ask[1])
            else:
                self.ask_do_you_have(pl_n, self.question_gonna_ask)

            self.game_state = GameState.QUESTION_CHOOSING
            self.next_turn()

    def ask_number_of(self, player, value):
        print("How many " + value + " cards " + countable[player] + " player have?")
        pl_n = player-1
        player_cards = self.cards[pl_n]

        #answer
        number = 0
        for card in player_cards:
            if (str(card[0]) == value) or (str(card[1]) == value):
                number += 1

        print(countable[player] + " player has " + str(number) + " " + value + " cards.")

        prop = "colour"
        if (len(value) == 1):
            prop = "number"

        self.kripke.apply_number_of_cards_anouncment(player, number, prop, value)

    def ask_do_you_have(self, player, card):
        print("Does " + countable[player] + " player have (" + ' '.join(card) + ")?")
        pl_n = player-1
        player_cards = self.cards[pl_n]

        #answer

        has = False
        for pl_card in player_cards:
            if (card[0] == pl_card[0]) and (card[1] == pl_card[1]):
                has = True

        print(countable[player] + " player " + has_or_not[has] + " (" + ' '.join(card) + ")")
        self.kripke.apply_single_card_anouncment(player, has, card[0], card[1])

    def get_possible_states_for_cur_player(self):
        player = self.current_turn_player
        return self.kripke.get_possible_cards(player+1, self.cards[player])

    def updateModel(self):
        pass

    def get_tips_for_cur_player(self):
        tool_tips = {}
        possible_players = [1, 2, 3]
        possible_players.remove(self.current_turn_player + 1)
        for q in self.players_questions[self.current_turn_player]:
            question = ' '.join(q)
            if len(q[0]) == 1: # 'do you have?' question
                possible_answers = [True, False]
                for player in possible_players:
                    for has in possible_answers:
                        tmp_states = self.kripke.apply_single_card_anouncment(player, has, q[0], q[1], just_test=True)
                        n = self.kripke.get_possible_words_number(self.current_turn_player+1, self.cards[self.current_turn_player], tmp_states)
                        key = (question, player, has)
                        tool_tips[key] = n
            else: # 'number of' question
                possible_answers = [0, 1, 2]
                prop = "colour"
                value = q[1]
                if (len(value) == 1):
                    prop = "number"
                for player in possible_players:
                    for ans in possible_answers:
                        tmp_states = self.kripke.apply_number_of_cards_anouncment(player, ans, prop, value, just_test=True)
                        n = self.kripke.get_possible_words_number(self.current_turn_player+1, self.cards[self.current_turn_player], tmp_states)
                        key = (question, player, ans)
                        tool_tips[key] = n
        return tool_tips



if __name__ == "__main__":

    x = GameModel()

    tips = x.get_tips_for_cur_player()

    p = 1
