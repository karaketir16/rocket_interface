import json
import sys

from PyQt5 import QtCore, QtWidgets, QtSerialPort
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QHBoxLayout, QAction, QStatusBar, QLineEdit, \
    QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSerialPort import QSerialPortInfo

from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

import datetime

from PyQt5.QtCore import QTimer,QDateTime


start_time = datetime.datetime.now()

class AddComport(QMainWindow):
    porttnavn = pyqtSignal(str)

    def __init__(self, parent, menu):
        super().__init__(parent)

        menuComporte = menu.addMenu("Comporte")

        info_list = QSerialPortInfo()
        serial_list = info_list.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        if (len(serial_ports) > 0):
            antalporte = len(serial_ports)
            antal = 0
            while antal < antalporte:
                button_action = QAction(serial_ports[antal], self)
                txt = serial_ports[antal]
                portinfo = QSerialPortInfo(txt)
                buttoninfotxt = " Ingen informationer"
                if portinfo.hasProductIdentifier():
                    buttoninfotxt = ("Produkt specifikation = " + str(portinfo.vendorIdentifier()))
                if portinfo.hasVendorIdentifier():
                    buttoninfotxt = buttoninfotxt + (" Fremstillers id = " + str(portinfo.productIdentifier()))
                button_action = QAction(txt, self)
                button_action.setStatusTip(buttoninfotxt)
                button_action.triggered.connect(lambda checked, txt=txt: self.valgAfComportClick(txt))
                menuComporte.addAction(button_action)
                antal = antal + 1
        else:
            print("Ingen com porte fundet")

    def valgAfComportClick(self, port):
        self.porttnavn.emit(port)

    def closeEvent(self, event):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.file = open(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S.txt"), "w")

        self.timer = QTimer()
        self.time_label = QtWidgets.QLabel(text="time")
        self.timer.timeout.connect(self.showTime)
        self.timer.start(500)

        self.graphWidget = pg.PlotWidget()

        self.rocket_title = QtWidgets.QLabel(text="Roket")
        self.rocket_title.setFont(QtGui.QFont("Arial", 20))

        self.rocket_state = QtWidgets.QLabel(text="state")
        self.speed_rocket = QtWidgets.QLabel(text="speed")
        self.abs_vert_acc = QtWidgets.QLabel(text="acc")
        self.gps_lat_rocket = QtWidgets.QLabel(text="gps_lat")
        self.gps_lon_rocket = QtWidgets.QLabel(text="gps_lon")
        self.pressure_rocket = QtWidgets.QLabel(text="pressure")
        self.altitude_rocket_text = QtWidgets.QLabel(text="altitude")
        self.max_altitude_rocket = QtWidgets.QLabel(text="max altitude")
        self.time_rocket = QtWidgets.QLabel(text="time")
        self.rssi_rocket = QtWidgets.QLabel(text="snr")
        self.empty = QtWidgets.QLabel(text="------------------------")

        self.payload_title = QtWidgets.QLabel(text="Faydalı Yük")
        self.payload_title.setFont(QtGui.QFont("Arial", 20))

        self.speed_payload = QtWidgets.QLabel(text="speed")
        self.gps_lat_payload = QtWidgets.QLabel(text="gps_lat")
        self.gps_lon_payload = QtWidgets.QLabel(text="gps_lon")
        self.pressure_payload = QtWidgets.QLabel(text="pressure")
        self.acc_x_payload = QtWidgets.QLabel(text="acc_x")
        self.acc_y_payload = QtWidgets.QLabel(text="acc_y")
        self.acc_z_payload = QtWidgets.QLabel(text="acc_z")
        self.temp_payload = QtWidgets.QLabel(text="temp")
        self.altitude_payload_text = QtWidgets.QLabel(text="altitude")
        self.time_payload = QtWidgets.QLabel(text="time")
        self.rssi_payload = QtWidgets.QLabel(text="snr")
        self.empty2 = QtWidgets.QLabel(text="-----------------------")

        # self.temp = QtWidgets.QLabel(text="temp")


        vlay = QtWidgets.QVBoxLayout()
        hlay = QtWidgets.QHBoxLayout()


        vlay.addWidget(self.rocket_title)
        vlay.addWidget(self.rocket_state)
        vlay.addWidget(self.abs_vert_acc)
        vlay.addWidget(self.speed_rocket)
        vlay.addWidget(self.gps_lat_rocket)
        vlay.addWidget(self.gps_lon_rocket)
        vlay.addWidget(self.pressure_rocket)
        vlay.addWidget(self.altitude_rocket_text)
        vlay.addWidget(self.max_altitude_rocket)
        vlay.addWidget(self.time_rocket)
        vlay.addWidget(self.rssi_rocket)

        vlay.addWidget(self.empty)

        vlay.addWidget(self.payload_title)
        vlay.addWidget(self.speed_payload)
        vlay.addWidget(self.gps_lat_payload)
        vlay.addWidget(self.gps_lon_payload)
        vlay.addWidget(self.pressure_payload)
        vlay.addWidget(self.acc_x_payload)
        vlay.addWidget(self.acc_y_payload)
        vlay.addWidget(self.acc_z_payload)
        vlay.addWidget(self.temp_payload)
        vlay.addWidget(self.altitude_payload_text)
        vlay.addWidget(self.time_payload)
        vlay.addWidget(self.rssi_payload)

        vlay.addWidget(self.empty2)

        vlay.addWidget(self.time_label)

        # vlay.addWidget(self.temp)

        hlay.addWidget(self.graphWidget)
        hlay.addLayout(vlay)


        # self.setCentralWidget(self.graphWidget)
        # self.setCentralWidget(centralWidget)

        self.seconds_rocket = []
        self.altitude_rocket = []

        self.seconds_payload = []
        self.altitude_payload = []

        #Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("Yükseklik zaman grafiği", color="b", size="30pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Yükseklik (metre)", **styles)
        self.graphWidget.setLabel("bottom", "Zaman (saniye)", **styles)
        #Add legend
        self.graphWidget.addLegend()

        #Add grid
        self.graphWidget.showGrid(x=True, y=True)

        pen1 = pg.mkPen(color=(255, 0, 0), width=10)
        pen2 = pg.mkPen(color=(0, 255, 0), width=10)
        self.plot_data_rocket = self.graphWidget.plot(self.seconds_rocket, self.altitude_rocket, pen=pen1, name="roket")
        self.plot_data_payload = self.graphWidget.plot(self.seconds_payload, self.altitude_payload, pen=pen2, name="payload")



        portname = "None"

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        comfinder = AddComport(self, menu)
        comfinder.porttnavn.connect(self.valgAfComport)

        self.setWindowTitle("Serial port display / send")

        self.output_te = QTextEdit(readOnly=True)
        self.button = QPushButton(
            text="Connect",
            checkable=True,
            toggled=self.on_toggled
        )
        lay = QVBoxLayout(self)
        lay.addLayout(hlay)

        lay.addWidget(self.output_te)
        lay.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

        self.serial = QtSerialPort.QSerialPort(
            portname,
            baudRate=QtSerialPort.QSerialPort.Baud38400,
            readyRead=self.receive)

        self.first = True

        self.received = ""
        self.dat = ""

    def showTime(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(time)
        self.timer.start(500)

    def bytes_str(self, d):
        return d if type(d) is str else "".join([chr(b) for b in d])

    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.bytesAvailable():
            text = self.bytes_str(bytes(self.serial.readAll()))
            self.received += text
            self.output_te.append(text)

        while len(self.received) > 0 and self.received[0] != '{':
            self.received = self.received[1:]

        if '}' in self.received:

            self.dat = ""
            while len(self.received) > 0 and self.received[0] != '#':
                self.dat += self.received[0]
                self.received = self.received[1:]


        self.showTime()
        print("".join(self.dat.split()))
        self.parsed = json.loads("".join(self.dat.split()))




        # print(self.parsed)

        if self.parsed["type"] == "rocket":

            self.seconds_rocket.append((datetime.datetime.now() - start_time).total_seconds())
            self.altitude_rocket.append(float(self.parsed["altitude"]))

            self.plot_data_rocket.setData(self.seconds_rocket, self.altitude_rocket)

            self.rocket_state.setText("Durum: " + str(self.parsed["state"]))
            self.speed_rocket.setText("Hız: " + str(self.parsed["speed"]) + " m/s")

            self.gps_lat_rocket.setText("GPS Enlem: " + str(self.parsed["gps_latitude"]))
            self.gps_lon_rocket.setText("GPS Boylam: " + str(self.parsed["gps_longtitude"]))

            self.abs_vert_acc.setText("Dikey İvme(dof): " + str(self.parsed["abs_vert_acc"]) + "m/s^2")
            # self.acc_y.setText("İvme Y: " + str(self.parsed["acc_y"]))
            # self.acc_z.setText("İvme Z: " + str(self.parsed["acc_z"]))

            self.pressure_rocket.setText("Basınç: " + str(self.parsed["pressure"]))

            self.altitude_rocket_text.setText("Yükseklik: " + str(self.parsed["altitude"]) + " m")
            self.max_altitude_rocket.setText("Max Yükseklik: " + str(max(self.altitude_rocket)) + " m")
            self.time_rocket.setText("Son Veri: " + datetime.datetime.now().strftime("%H:%M:%S"))
            self.rssi_rocket.setText("RSSI: " + str(self.parsed["rssi"]) + " dBm")
            # self.temp.setText("Sıcaklık" + str(self.parsed["temp"]))

        elif self.parsed["type"] == "payload":
            self.seconds_payload.append((datetime.datetime.now() - start_time).total_seconds())
            self.altitude_payload.append(float(self.parsed["altitude"]))
            # self.altitude_payload.append(float(0))

            self.plot_data_payload.setData(self.seconds_payload, self.altitude_payload)

            self.speed_payload.setText("Hız: " + str(self.parsed["speed"]) + " m/s")
            self.gps_lat_payload.setText("GPS Enlem: " + str(self.parsed["gps_latitude"]))
            self.gps_lon_payload.setText("GPS Boylam: " + str(self.parsed["gps_longtitude"]))

            self.acc_x_payload.setText("İvme X: " + str(self.parsed["acc_x"]) + "m/s^2")
            self.acc_y_payload.setText("İvme Y: " + str(self.parsed["acc_y"]) + "m/s^2")
            self.acc_z_payload.setText("İvme Z: " + str(self.parsed["acc_z"]) + "m/s^2")

            self.pressure_payload.setText("Basınç: " + str(self.parsed["pressure"]))
            self.temp_payload.setText("Sıcaklık: " + str(self.parsed["temp"]))

            self.altitude_payload_text.setText("Yükseklik: " + str(self.parsed["altitude"]) + " m")
            self.time_payload.setText("Son Veri: " + datetime.datetime.now().strftime("%H:%M:%S"))
            self.rssi_payload.setText("RSSI: " + str(self.parsed["rssi"]) + " dBm")

        self.file.write("".join(self.dat.split()) + str("\n"))




    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.button.setText("Disconnect" if checked else "Connect")
        if checked:
            if not self.serial.isOpen():
                self.serial.open(QtCore.QIODevice.ReadWrite)
                if not self.serial.isOpen():
                    self.button.setChecked(False)
            else:
                self.button.setChecked(False)
        else:
            self.serial.close()

    def valgAfComport(self, nyport):
        seropen = False
        if self.serial.isOpen():
            seropen = True
            self.serial.close()
        self.serial.setPortName(nyport)
        if seropen:
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if not self.serial.isOpen():
                self.button.setChecked(False)

        print(nyport)

    def closeEvent(self, event):
        self.serial.close()
        print("Comport lukket")
        # print(comporttxt)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
