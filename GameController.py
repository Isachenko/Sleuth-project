from BoardView import BoardView
from GameModel import GameModel
from GameModel import GameState
from PackView import PackView
from QuestionsView import QuestionView
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSlot


class GameController():

    def __init__(self, app):
        self.restart_pressed = False
        self.already_won = False
        self.total_cur_words_n = 0
        self.app = app
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

        self.board_view = BoardView(self.player_views, self.open_view, self.hidden_view, self.question_view)

        self.question_view.question_clicked.connect(self.question_button_clicked)
        self.board_view.next_turn_button.clicked.connect(self.nex_player_button_clicked)
        self.board_view.restart_button.clicked.connect(self.restart_clicked)

        self.update_tables_for_cur_player()
        self.update_tips()
        self.update_views()


        self.board_view.next_turn_button.setDisabled(True)

    def start(self):
        self.board_view.showMaximized()
        self.app.exec_()
        return self.restart_pressed

    def question_button_clicked(self, str):
        if str.lower().startswith("player"):
            self.game_model.player_to_ask_choosen(str)
            self.update_tables_for_cur_player()
            self.question_view.disable_all()
            self.update_views()
            self.update_tips()
            self.board_view.next_turn_button.setEnabled(True)
        else:
            question = str.split(" ")
            self.game_model.question_chosen(question)
            self.question_view.change_player_question_mode(False)
            #self.update_views()
            #self.update_tips()

    def update_views(self):
        if not self.already_won:
            self.question_view.set_questions(self.game_model.get_cuurent_player_questions())
            info_text = ""
            answer_text = " "
            if self.game_model.game_state == GameState.PLAYER_TO_ASK_CHOOSING:
                question = ''.join(s+" " for s in self.game_model.question_gonna_ask)
                info_text = "Question is {}. Choose the player to ask".format(question)
            elif self.game_model.game_state == GameState.QUESTION_CHOOSING:
                self.question_view.hide_player_button_but_show_others(self.game_model.current_turn_player)
                info_text = "Choose the question to ask"
            elif self.game_model.game_state == GameState.CURRENT_PLAYER_FINISHED:
                info_text = "click 'Next player' when you finished"
                answer_text = "Answer: " + self.game_model.last_answer

            self.board_view.info_label.setText("Player {} turn. ".format(self.game_model.current_turn_player+1) + info_text)
            self.board_view.answer_label.setText(answer_text)

            self.update_hide_show_views()
            self.update_tables_for_cur_player()


    def update_hide_show_views(self):
        for i, view in enumerate(self.player_views):
            if (i == self.game_model.current_turn_player):
                view.switch_to_open_view()
            else:
                view.switch_to_hidden_view()

    def update_tables_for_cur_player(self):
        possible_variant, varian_numbers, total_number = self.game_model.get_possible_states_for_cur_player()
        self.total_cur_words_n = total_number
        self.hidden_view.update_tables(possible_variant[0], varian_numbers[0], total_number)
        for i, view in enumerate(self.player_views):
            if i != self.game_model.current_turn_player:
                view.update_tables(possible_variant[i+1], varian_numbers[i+1], total_number)

        if (len(possible_variant[0]) == 1) and not self.already_won:
            self.already_won = True
            self.hidden_view.show_both()
            self.board_view.restart_button.show()
            self.board_view.next_turn_button.hide()
            self.board_view.answer_label.hide()
            self.board_view.info_label.setText("Player {} won, congratulation!!!. To play again press 'Restart' button".format(self.game_model.current_turn_player + 1))

    def update_tips(self):
        tips = self.game_model.get_tips_for_cur_player()

        players = [1,2,3]
        players.remove(self.game_model.current_turn_player+1)

        self.question_view.setTips(tips, players, self.total_cur_words_n)

    def nex_player_button_clicked(self):
        self.game_model.next_turn()
        self.game_model.start_turn()
        self.update_views()
        self.update_tips()
        self.question_view.change_player_question_mode(True)
        self.board_view.next_turn_button.setDisabled(True)

    def restart_clicked(self):
        self.restart_pressed = True
        self.app.quit()





