from PyQt5 import QtWidgets
from CardView import CardView


class PackView(QtWidgets.QWidget):

    def __init__(self, name, cards):
        super().__init__()

        self.name_label = QtWidgets.QLabel(name)
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addStretch()
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()

        cards_layout = QtWidgets.QHBoxLayout()
        for card in cards:
            card_view = CardView(card[0], card[1])
            cards_layout.addWidget(card_view)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(name_layout)
        v_box.addLayout(cards_layout)


        self.setLayout(v_box)

