from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox,  QPushButton, QWidget, QComboBox, QGridLayout, QLabel, QFileDialog
import matplotlib.pyplot as plt


class PlotWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUI()


    def setupUI(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        refreshButton = QPushButton("Выбрать")
        refreshButton.clicked.connect(self.choose_directory)
        refreshButton.setMaximumWidth(150)
        refreshButton.setMinimumWidth(150)
        self.layout.addWidget(refreshButton, 5, 0)

        self.image = QLabel()
        self.layout.addWidget(self.image, 0, 0, 5, 1)


    def choose_directory(self):
        input_dir = QFileDialog.getOpenFileName()
        I = []
        U = []

        absPath = input_dir[0].split("/")

        path = absPath[-2] + "/" + absPath[-1]

        with open(path, "r") as file:
            for line in file:
                I.append(int(line.split(" ")[0]))
                U.append(int(line.split(" ")[1]))

        print("U = ", U)
        print("I = ", I)

        plt.figure()
        plt.subplot(211)
        plt.plot(range(len(U)), U)
        plt.title("Напряжение")

        plt.subplot(212)
        plt.title("Ток")
        plt.plot(range(len(I)), I)
        plt.tight_layout()
        plt.savefig("plot.png")

        self.image.setPixmap(QPixmap("plot.png"))

