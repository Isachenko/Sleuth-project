from BoardView import BoardView
from GameModel import GameModel
from PackView import PackView
import sys
from PyQt5 import QtWidgets, QtGui


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


        self.board_view = BoardView(self.player_views, self.open_view, self.hidden_view)

        self.game_model

    def start(self):
        self.board_view.show()
        sys.exit(self.app.exec_())
