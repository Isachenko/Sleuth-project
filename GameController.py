from BoardView import BoardView
from GameModel import GameModel
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
        for cards in self.game_model.cards:
            name = "name"
            self.player_views.append(PackView(name, cards))

        self.open_view = PackView("open", self.game_model.cards_open)
        self.hidden_view = PackView("hidden", self.game_model.cards_hidden)
        self.question_view = QuestionView(self.game_model.questions_in_hand_number)
        self.question_view.set_questions(self.game_model.players_questions[0])

        self.question_view.question_clicked.connect(self.question_button_clicked)

        self.board_view = BoardView(self.player_views, self.open_view, self.hidden_view, self.question_view)

    def start(self):
        self.board_view.show()
        sys.exit(self.app.exec_())


    def question_button_clicked(self, str):
        question = str.split(" ")
        self.game_model.question_chosen(question)
        self.game_model.next_turn()
        self.updateQuestionsView()

    def updateQuestionsView(self):
        self.question_view.set_questions(self.game_model.get_cuurent_player_questions())

