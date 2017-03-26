from BoardView import BoardView
from GameModel import GameModel
from GameModel import GameState
from PackView import PackView
from QuestionsView import QuestionView
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSlot


class GameController():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.game_model = GameModel()

        self.player_views = []
        for i, cards in enumerate(self.game_model.cards):
            name = "player {}".format(i+1)
            self.player_views.append(PackView(name, cards))


        self.open_view = PackView("open", self.game_model.cards_open)
        self.open_view.switch_to_open_view()
        self.hidden_view = PackView("hidden", self.game_model.cards_hidden)
        self.hidden_view.switch_to_hidden_view()

        self.question_view = QuestionView(self.game_model.questions_in_hand_number, self.game_model.players_number)
        self.question_view.set_questions(self.game_model.players_questions[0])

        self.question_view.question_clicked.connect(self.question_button_clicked)

        self.board_view = BoardView(self.player_views, self.open_view, self.hidden_view, self.question_view)
        self.update_tables_for_cur_player()
        self.update_views()

    def start(self):
        self.board_view.show()
        sys.exit(self.app.exec_())


    def question_button_clicked(self, str):
        if str.lower().startswith("player"):
            self.game_model.player_to_ask_choosen(str)
            self.update_tables_for_cur_player()
            self.update_views()
        else:
            question = str.split(" ")
            self.game_model.question_chosen(question)
            self.update_views()

    def update_views(self):
        self.question_view.set_questions(self.game_model.get_cuurent_player_questions())
        info_text = ""
        if self.game_model.game_state == GameState.PLAYER_TO_ASK_CHOOSING:
            question = ''.join(s+" " for s in self.game_model.question_gonna_ask)
            info_text = "Question is {}. Chose the player to ask".format(question)
        elif self.game_model.game_state == GameState.QUESTION_CHOOSING:
            self.question_view.hide_player_button_but_show_others(self.game_model.current_turn_player)
            info_text = "Chose the question to ask"

        self.board_view.info_label.setText("Player {} turn: ".format(self.game_model.current_turn_player+1) + info_text)

        self.update_hide_show_views()

    def update_hide_show_views(self):
        for i, view in enumerate(self.player_views):
            if (i == self.game_model.current_turn_player):
                view.switch_to_open_view()
            else:
                view.switch_to_hidden_view()

    def update_tables_for_cur_player(self):
        possible_variant, varian_numbers, total_number = self.game_model.get_possible_states_for_cur_player()
        self.hidden_view.update_tables(possible_variant[0], varian_numbers[0], total_number)
        for i, view in enumerate(self.player_views):
            if (i != self.game_model.current_turn_player):
                view.update_tables(possible_variant[i+1], varian_numbers[i+1], total_number)




