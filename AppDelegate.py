import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox, QApplication, QWidget, QTabWidget, QGridLayout,\
    QInputDialog, QLineEdit, QPushButton
from SettingsWidget import SettingsWidget
from PlotWidget import PlotWidget


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Магнитная плетизмография'
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтвердите действие',
                                     "Вы уверены, что хотите закрыть программу?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = SettingsWidget(parent)
        self.tab2 = PlotWidget(parent)

        # Add tabs
        self.tabs.addTab(self.tab1, "")
        self.tabs.addTab(self.tab2, "")


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('ФИО пациента', self)
        self.btn.move(20, 20)
        self.btn.resize(200, 30)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setStyleSheet("""
                QPushButton{
                    font-style: oblique;
                    font-weight: bold;
                    border: 1px solid #1DA1F2;
                    border-radius: 15px;
                    color: navy;
                    background-color: lavenderblush;
                }
                """)

        self.le = QLineEdit(self)
        self.le.move(230, 20)
        self.le.resize(300, 30)


        #self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Введите ФИО пациента:')

        if ok and text !='':
            self.le.setText(str(text))









if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())