'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class PlotWidget(QWidget):

    def __init__(self):
        super(PlotWidget,self).__init__()

        self.figure = plt.figure()
        plt.subplots_adjust(top=0.95,left=0.15,right=0.95,bottom=0.15)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.actions

        self._layout = QVBoxLayout()
        self._layout.addWidget(self.toolbar)
        self._layout.addWidget(self.canvas)
        self.setLayout(self._layout)

if __name__ == '__main__':
    app = QApplication([])
    widget = PlotWidget(parent=None)
    widget.show()
    app.exec_()
