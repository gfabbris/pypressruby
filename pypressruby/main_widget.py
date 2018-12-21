'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QGridLayout,QMessageBox

from modules.plot_widget import PlotWidget
from modules.options_widget import OptionsWidget
from modules.widgets_logic import LogicWidgets

from time import sleep

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        self.spec_fname= ''
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Ruby Pressure Calibration')
        self.setGeometry(200, 200, 1000, 600)
        
        optwidth = 300
        
        self.plot_widget = PlotWidget()
        self.plot_widget.setFixedWidth(1000-optwidth)
        
        self.options_widget = OptionsWidget()
        self.options_widget.setFixedWidth(optwidth)
        
        self._layout = QGridLayout()
        self._layout.addWidget(self.options_widget,0,0)
        self._layout.addWidget(self.plot_widget,0,1,1,5)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(self._layout)
        
        self.connections = LogicWidgets(self.statusBar(),self.options_widget,
                                        self.plot_widget)
        
    def closeEvent(self, event):
        
        close = QMessageBox()
        close.setText("Are you sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            self.connections.stop_spectrometer()
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()

