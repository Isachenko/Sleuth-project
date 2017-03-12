from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

class QuestionView(QtWidgets.QWidget):

    question_clicked = pyqtSignal(str)

    def __init__(self, questions_number):
        super().__init__()

        self.question_buttons = []

        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        for i in range(questions_number):
            button = QtWidgets.QPushButton("question?")
            button.clicked.connect(self.button_clicked_handler)
            layout.addWidget(button)
            self.question_buttons.append(button)
        layout.addStretch()

        label_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Questins")
        label_layout.addStretch()
        label_layout.addWidget(label)
        label_layout.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(label_layout)
        v_box.addLayout(layout)

        self.setLayout(v_box)

    def set_questions(self, questions):
        i = 0
        for button in self.question_buttons:
            button.setText(questions[i][0] + " " + questions[i][1])
            i += 1

    def button_clicked_handler(self):
        text = self.sender().text()
        self.question_clicked.emit(text)


