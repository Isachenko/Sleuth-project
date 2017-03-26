from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

class QuestionView(QtWidgets.QWidget):

    question_clicked = pyqtSignal(str)

    def __init__(self, questions_number, players_number):
        super().__init__()

        self.question_buttons = []

        layout = QtWidgets.QHBoxLayout()
        #layout.addStretch()
        questions_label = QtWidgets.QLabel("Questins:")
        layout.addWidget(questions_label)
        for i in range(questions_number):
            button = QtWidgets.QPushButton("question")
            button.clicked.connect(self.button_clicked_handler)
            layout.addWidget(button)
            self.question_buttons.append(button)
        layout.addStretch()


        selected_player_layout = QtWidgets.QHBoxLayout()
        #selected_player_layout.addStretch()
        selected_player_label = QtWidgets.QLabel("Seletct player to ask")
        selected_player_layout.addWidget(selected_player_label)
        self.players_buttons = dict()
        for i in range(players_number):
            button = QtWidgets.QPushButton("player {0}".format(i+1))
            button.clicked.connect(self.button_clicked_handler)
            selected_player_layout.addWidget(button)
            self.players_buttons[i] = button
        selected_player_layout.addStretch()



        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(selected_player_layout)
        v_box.addLayout(layout)

        self.setLayout(v_box)
        self.change_player_question_mode(True)

    def set_questions(self, questions):
        i = 0
        for button in self.question_buttons:
            button.setText(questions[i][0] + " " + questions[i][1])
            i += 1

    def button_clicked_handler(self):
        text = self.sender().text()
        self.question_clicked.emit(text)

    def hide_player_button_but_show_others(self, player_num):
        for pl_num, button in self.players_buttons.items():
            if (pl_num == player_num):
                button.hide()
            else:
                button.show()

    def change_player_question_mode(self, question=True):
        for pl_num, button in self.players_buttons.items():
            button.setDisabled(question)

        for button in self.question_buttons:
            button.setEnabled(question)




