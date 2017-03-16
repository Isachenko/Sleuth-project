from PyQt5 import QtWidgets
from CardView import CardView


class PackView(QtWidgets.QWidget):

    def __init__(self, name, cards):
        super().__init__()

        self.name_label = QtWidgets.QLabel(name)

        #open view
        self.open_widgets = []

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addStretch()
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()

        self.cards_layout = QtWidgets.QHBoxLayout()
        for card in cards:
            card_view = CardView(card[0], card[1])
            self.cards_layout.addWidget(card_view)
            self.open_widgets.append(card_view)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(name_layout)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(self.cards_layout)

        #hidden view
        self.table = QtWidgets.QTableView()
        h_box.addWidget(self.table)

        v_box.addLayout(h_box)
        self.setLayout(v_box)



    def switch_to_hidden_view(self):
        for w in self.open_widgets:
            w.hide()
        self.table.show()

    def switch_to_open_view(self):

        for w in self.open_widgets:
            w.show()
        self.table.hide()

