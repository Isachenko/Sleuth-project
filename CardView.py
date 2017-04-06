from PyQt5 import QtWidgets
from PyQt5 import QtCore


class CardView(QtWidgets.QWidget):

    def __init__(self, type, colour):
        super().__init__()

        self.label = QtWidgets.QLabel(type + " " + colour)
        style = "background-color: {0}; color: white".format(colour)
        self.label.setStyleSheet(style)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.v_box = QtWidgets.QVBoxLayout()
        self.v_box.addWidget(self.label)
        self.setLayout(self.v_box)

