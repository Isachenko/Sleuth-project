from GameController import GameController
#self.b.clicked.connect(self.button_clicked)
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR
from PyQt5 import QtWidgets
import sys



if __name__ == "__main__":
    print("Qt version:", QT_VERSION_STR)
    print("SIP version:", SIP_VERSION_STR)
    print("PyQt version:", PYQT_VERSION_STR)

    app = QtWidgets.QApplication(sys.argv)
    controller = GameController(app)
    #controller.start() return True if is ended by restart button
    while (controller.start()):
        controller = GameController(app)
        print("restart")

