from PyQt5 import QtWidgets
from CardView import CardView
from PyQt5 import QtGui
from PyQt5 import  QtCore



class PackView(QtWidgets.QWidget):


    def __init__(self, name, cards):
        self.colour_to_j = {"red": 0, "green": 1, "blue": 2}
        self.colour_to_qt_colour = {"red": QtCore.Qt.red, "green": QtCore.Qt.green, "blue": QtCore.Qt.blue}

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
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("red"))
        self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("green"))
        self.table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("blue"))
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

    def update_tables(self, possible_variant):
        self.table.clearContents()
        for number, colour in possible_variant:
            i = int(number) - 1
            j = self.colour_to_j[colour]
            item = QtWidgets.QTableWidgetItem("Possible")
            #item.setBackground(QtCore.Qt.red)
            item.setBackground(self.colour_to_qt_colour[colour])
            item.setForeground(QtCore.Qt.white)
            self.table.setItem(i, j, item)

