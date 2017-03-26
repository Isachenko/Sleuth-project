from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore

class QuestionView(QtWidgets.QWidget):

    question_clicked = pyqtSignal(str)

    def __init__(self, questions_number, players_number):
        super().__init__()

        self.question_buttons = []
        self.tips_tables = []

        layout = QtWidgets.QHBoxLayout()
        #layout.addStretch()
        questions_label = QtWidgets.QLabel("Questins:")
        layout.addWidget(questions_label)
        for i in range(questions_number):
            button = QtWidgets.QPushButton("question")
            button.clicked.connect(self.button_clicked_handler)

            table = QtWidgets.QTableWidget()
            self.tips_tables.append(table)
            table.setColumnCount(2)

            v_box_l = QtWidgets.QVBoxLayout()
            v_box_l.addWidget(button)
            v_box_l.addWidget(table)

            layout.addLayout(v_box_l)
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

    def setToolTips(self, tooltips):
        for buttons in self.question_buttons:
            key = buttons.text
            buttons.setToolTip(tooltips[key])


    def setTips(self, tips, players, total_words):
        headers_for_number_of = ["0", "1", "2"]
        headers_for_tf = ["False", "True"]

        for tip_table in self.tips_tables:
            tip_table.setHorizontalHeaderLabels(["player " + str(i) for i in players])

        for i, tip_table in enumerate(self.tips_tables):
            if "number_of" in self.question_buttons[i].text():
                tip_table.setRowCount(3)
                tip_table.setVerticalHeaderLabels(headers_for_number_of)
            else:
                tip_table.setRowCount(2)
                tip_table.setVerticalHeaderLabels(headers_for_tf)

        for key, value in tips.items():
            q = key[0]
            pl = key[1]
            ans = key[2]
            for i, tip_table in enumerate(self.tips_tables):
                if self.question_buttons[i].text() == q:
                    i = 0
                    if "number_of" in q:
                        i = ans
                    else:
                        i = int(ans)
                    j = players.index(pl)
                    text = str(value)
                    item = QtWidgets.QTableWidgetItem()
                    if value == 0:
                        text = "impossible"
                        item.setBackground(QtCore.Qt.red)
                        item.setForeground(QtCore.Qt.white)
                    if value == total_words:
                        text = "no sense"
                        item.setBackground(QtCore.Qt.red)
                        item.setForeground(QtCore.Qt.white)
                    item.setText(text)
                    tip_table.setItem(i, j, item)


