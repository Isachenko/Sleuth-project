import sys
from PyQt5 import QtWidgets, QtGui
from PackView import PackView
from BoardView import BoardView


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.players_views = []
        self.players_views.append(PackView('Adrian', [['1', "red"],['2',"blue"]]))
        self.players_views.append(PackView('Andrei', [['2', "green"],['2',"red"]]))
        self.players_views.append(PackView('Wouter', [['3', "green"],['1',"blue"]]))

        self.hidden_view = PackView('hidden', [['3', "red"]])
        self.open_view = PackView('open', [['3', "blue"], ['1', 'green']])

        self.board_view = BoardView(self.players_views, self.hidden_view, self.open_view)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.board_view)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('Very nice title')

        self.show()

        #self.b.clicked.connect(self.button_clicked)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())
