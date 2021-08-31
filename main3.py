from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()


        self.text1 = QtWidgets.QLabel(text="Text1")
        self.text2 = QtWidgets.QLabel(text="Text2")

        vlay = QtWidgets.QVBoxLayout()
        hlay = QtWidgets.QHBoxLayout()

        vlay.addWidget(self.text1)
        vlay.addWidget(self.text2)

        hlay.addWidget(self.graphWidget)
        hlay.addLayout(vlay)

        widget = QtWidgets.QWidget()
        widget.setLayout(hlay)
        self.setCentralWidget(widget)

        # self.setCentralWidget(self.graphWidget)
        # self.setCentralWidget(centralWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

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

        pen = pg.mkPen(color=(255, 0, 0), width=15)
        self.plot_data = self.graphWidget.plot(hour, temperature, pen=pen)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()