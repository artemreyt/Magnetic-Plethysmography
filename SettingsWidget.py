from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMessageBox,  QPushButton, QWidget, QComboBox, QGridLayout, QLabel
from PyQt5.QtCore import Qt
import os
import serial.tools.list_ports
import measurment
import serial.tools.list_ports
import time
import threading

rootPath = os.getcwd()

speeds = ["921600", "430800", "9600", "19200"]

# CONSTANTS !!!!!
byteSize = ["5", "6", "7", "8"]
parity = ["Нет", "Чет", "Нечет"]
stopBits = ["1", "1.5", "2"]


class SettingsWidget(QWidget):

    running = False

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUI()
        self.updateConnectedDevices()

    def setupUI(self):

        icons_path = rootPath + "/icons"
        if not os.path.exists(icons_path):
            os.mkdir(icons_path)
        os.chdir(icons_path)

        # Label's font
        boldFont = QFont()
        boldFont.setBold(True)
        boldFont.setPixelSize(14)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPixelSize(18)

        italFont = QFont()
        italFont.setPixelSize(14)
        italFont.setItalic(True)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        titleLabel = QLabel("Настройки подключения")
        titleLabel.setFont(titleFont)
        titleLabel.setMaximumHeight(18)
        titleLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLabel, 0, 1)


        deviceLabel = QLabel("Устройство")
        deviceLabel.setFont(boldFont)
        self.layout.addWidget(deviceLabel, 1, 0)

        self.devicesBox = QComboBox()
        self.layout.addWidget(self.devicesBox, 1, 1)


        refreshButton = QPushButton("Обновить")
        refreshButton.clicked.connect(self.updateConnectedDevices)
        refreshButton.setMaximumWidth(150)
        refreshButton.setMinimumWidth(150)
        refreshButton.setIcon(QIcon("refresh.png"))
        self.layout.addWidget(refreshButton, 1, 2)


        speedLabel = QLabel("Скорость")
        speedLabel.setFont(boldFont)
        self.layout.addWidget(speedLabel, 2, 0)

        self.speedBox = QComboBox()
        self.speedBox.addItems(speeds)
        self.layout.addWidget(self.speedBox, 2, 1)


        byteSizeLabel = QLabel("Размер байта")
        byteSizeLabel.setFont(boldFont)
        self.layout.addWidget(byteSizeLabel, 3, 0)

        self.byteSizeBox = QComboBox()
        self.byteSizeBox.addItems(byteSize)
        self.layout.addWidget(self.byteSizeBox, 3, 1)


        parityLabel = QLabel("Паритет")
        parityLabel.setFont(boldFont)
        self.layout.addWidget(parityLabel, 4, 0)

        self.parityBox = QComboBox()
        self.parityBox.addItems(parity)
        self.layout.addWidget(self.parityBox, 4, 1)


        stopBitsLabel = QLabel("Стоп-битов")
        stopBitsLabel.setFont(boldFont)
        self.layout.addWidget(stopBitsLabel, 5, 0)

        self.stopBitsBox = QComboBox()
        self.stopBitsBox.setMinimumWidth(300)
        self.stopBitsBox.addItems(stopBits)
        self.layout.addWidget(self.stopBitsBox, 5, 1)


        stateStaticLabel = QLabel("Состояние")
        stateStaticLabel.setFont(boldFont)
        stateStaticLabel.setMaximumHeight(70)
        self.layout.addWidget(stateStaticLabel, 6, 0)

        self.stateLabel = QLabel()
        self.stateLabel.setText("Отключено")
        self.stateLabel.setFont(italFont)
        self.layout.addWidget(self.stateLabel, 6, 1)


        self.startButton = QPushButton("Начать")
        self.startButton.setMaximumWidth(150)
        self.startButton.setMinimumWidth(150)
        self.startButton.setIcon(QIcon("bluetooth-on.png"))
        self.startButton.clicked.connect(self.startMeasurment)
        self.layout.addWidget(self.startButton, 6, 2)


        self.stopButton = QPushButton("Прервать")
        self.stopButton.setMaximumWidth(150)
        self.stopButton.setMinimumWidth(150)
        self.stopButton.setIcon(QIcon("bluetooth-off.png"))
        self.stopButton.clicked.connect(self.stopMeasurment)
        self.stopButton.setHidden(True)
        self.layout.addWidget(self.stopButton, 6, 2)


        self.calibrationButton = QPushButton("Калибровка")
        self.calibrationButton.setMaximumWidth(150)
        self.calibrationButton.setMinimumWidth(150)
        self.calibrationButton.setIcon(QIcon("magnifier.png"))
        self.calibrationButton.clicked.connect(self.calibration)
        self.layout.addWidget(self.calibrationButton, 7, 2)

        self.singleMeasurmentButton = QPushButton("Единичное измерение")
        self.singleMeasurmentButton.setIcon(QIcon("play.png"))
        self.singleMeasurmentButton.clicked.connect(self.singleMeasurment)
        self.layout.addWidget(self.singleMeasurmentButton, 7, 1)

        os.chdir(rootPath)

    def singleMeasurment(self):

        selectedDevice = self.devicesBox.currentText()
        selectedSpeed = int(self.speedBox.currentText())
        # selectedStopBits = int(self.stop.currentText())
        # selectedByteSize = int(self.byteSizeBox.currentText())
        dirName = str(time.ctime()).replace(":", "-")
        try:
            measurment.run(
                port=selectedDevice,
                speed=selectedSpeed,
                dirName=dirName
            )

        except Exception as error:
            print(error)
            QMessageBox.question(self, 'Уведомление',
                                 "Не удалось подключиться к %s" % selectedDevice, QMessageBox.Ok |
                                 QMessageBox.Ok)

    def calibration(self):
        selectedDevice = self.devicesBox.currentText()
        selectedSpeed = int(self.speedBox.currentText())
        measurment.calibration(selectedDevice, selectedSpeed)

    def stopMeasurment(self):
        self.running = False
        self.stateLabel.setText("Отключено")
        self.stopButton.setHidden(True)
        self.startButton.setHidden(False)


    def startMeasurment(self):
        self.running = True
        self.stopButton.setHidden(False)
        self.startButton.setHidden(True)
        self.stateLabel.setText("Проводятся измерения")

        selectedDevice = self.devicesBox.currentText()
        selectedSpeed = int(self.speedBox.currentText())
        # selectedStopBits = int(self.stop.currentText())
        # selectedByteSize = int(self.byteSizeBox.currentText())
        dirName = str(time.ctime()).replace(":", "-")

        def thread():
            i = 1
            while self.running:
                try:
                    measurment.run(
                        port=selectedDevice,
                        speed=selectedSpeed,
                        dirName=dirName,
                        num=i,
                        uGraph=False,
                        iGraph=False
                    )
                    i += 1
                except Exception as error:
                    print(error)


                time.sleep(10)

        threading.Thread(target=thread).start()


    def updateConnectedDevices(self):
        self.devicesBox.clear()

        list = serial.tools.list_ports.comports()
        connected = []
        for element in list:
            connected.append(element.device)

        self.devicesBox.addItems(connected)
