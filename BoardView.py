from PyQt5 import QtWidgets


class BoardView(QtWidgets.QWidget):

    def __init__(self, players_views, open_cards_view, hidden_view):
        super().__init__()

        players_layout = QtWidgets.QHBoxLayout()
        players_layout.addStretch()
        for view in players_views:
            players_layout.addWidget(view)
        players_layout.addStretch()

        open_cards_layout = QtWidgets.QHBoxLayout()
        open_cards_layout.addWidget(open_cards_view)

        hidden_cards_layout = QtWidgets.QHBoxLayout()
        hidden_cards_layout.addWidget(hidden_view)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(players_layout)
        v_box.addLayout(open_cards_layout)
        v_box.addLayout(hidden_cards_layout)

        self.setLayout(v_box)

