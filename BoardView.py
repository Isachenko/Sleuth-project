from PyQt5 import QtWidgets


class BoardView(QtWidgets.QWidget):

    def __init__(self, players_views, open_cards_view, hidden_view, questions_view):
        super().__init__()

        players_layout = QtWidgets.QHBoxLayout()
        #players_layout.addStretch()
        for view in players_views:
            players_layout.addWidget(view)
        #players_layout.addStretch()

        hidden_open_cards_layout = QtWidgets.QHBoxLayout()
        hidden_open_cards_layout.addWidget(open_cards_view)
        hidden_open_cards_layout.addWidget(hidden_view)

        current_player_questions_layout = QtWidgets.QHBoxLayout()
        current_player_questions_layout.addWidget(questions_view)



        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(players_layout)
        v_box.addLayout(hidden_open_cards_layout)
        v_box.addLayout(current_player_questions_layout)
        self.info_label = QtWidgets.QLabel("Info:")
        v_box.addWidget(self.info_label)
        v_box.addLayout(current_player_questions_layout)


        self.setLayout(v_box)
        self.setWindowTitle("Sleuth")

