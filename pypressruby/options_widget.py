'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QApplication, QWidget,QGroupBox,QComboBox
from PyQt5.QtWidgets import QLabel,QTextEdit,QPushButton,QCheckBox,QSpinBox
from PyQt5.QtWidgets import QGridLayout,QVBoxLayout,QHBoxLayout,QDoubleSpinBox

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont

class OptionsWidget(QWidget):

    def __init__(self):
        super(OptionsWidget,self).__init__()
        
        self.spectrometer = SpectrometerWidget()
        self.graph = GraphWidget()
        self.pressure = PressureWidget()
        
        self._layout = QVBoxLayout()
        self._layout.addWidget(self.spectrometer)
        self._layout.addWidget(self.graph)
        self._layout.addWidget(self.pressure)
        self.setLayout(self._layout)

class SpectrometerWidget(QGroupBox):

    def __init__(self,title='Spectrometer Controls',fontsize=18):
        
        super(SpectrometerWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
    def build_widgets(self):
        
        self.spec_name = QComboBox()
    
        self.reload_button = QPushButton('Reload')

        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')
        
        self.dark_button = QPushButton('Collect Dark')
        self.dark_label = QLabel('Remove dark?')
        self.dark_box = QCheckBox()
        self.dark_box.setChecked(False)
        
        self.integrate_label = QLabel('Integration time (msec):')
        self.integrate = QTextEdit('100')
        self.integrate.setMaximumHeight(25)
        self.integrate.setMaximumWidth(80)
    
    def build_layout(self):

        self._layout = QVBoxLayout()
        
        self._layout_spec = QHBoxLayout()
        self._layout_spec.addWidget(self.spec_name,2)
        self._layout_spec.addWidget(self.reload_button,1)
        
        self._layout_buttons = QHBoxLayout()
        self._layout_buttons.addWidget(self.start_button)
        self._layout_buttons.addWidget(self.stop_button)
        
        self._layout_dark = QHBoxLayout()
        self._layout_dark.addWidget(self.dark_button)
        self._layout_dark.addWidget(self.dark_label)
        self._layout_dark.addWidget(self.dark_box)
        
        self._layout_integrate = QHBoxLayout()
        self._layout_integrate.addWidget(self.integrate_label)
        self._layout_integrate.addWidget(self.integrate)

        self._layout.addLayout(self._layout_spec)
        self._layout.addLayout(self._layout_buttons)
        self._layout.addLayout(self._layout_dark)
        self._layout.addLayout(self._layout_integrate)
        
        self.setLayout(self._layout)

class GraphWidget(QGroupBox):
    
    def __init__(self,title='Graph Options'):
        
        super(GraphWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
    def build_widgets(self):

        self.limitlabel = QLabel('Limits')
        
        self.minlabel = QLabel('Min.')
        self.maxlabel = QLabel('Max.')
        
        self.x_axis = QLabel('x axis')
        self.y_axis = QLabel('y axis')
        
        #self.xmin = QTextEdit('690')
        self.xmin = QDoubleSpinBox()
        self.xmin.setMaximum(900)
        self.xmin.setMinimum(600)
        self.xmin.setValue(690)
        self.xmin.setDecimals(1)
        self.xmin.setMaximumHeight(25)
        self.xmin.setMaximumWidth(100)
        
        #self.xmax = QTextEdit('700')
        self.xmax = QDoubleSpinBox()
        self.xmax.setMaximum(900)
        self.xmax.setMinimum(600)
        self.xmax.setValue(700)
        self.xmax.setDecimals(1)
        self.xmax.setMaximumHeight(25)
        self.xmax.setMaximumWidth(100)
        
        #self.ymin = QTextEdit('0')
        self.ymin = QSpinBox()
        self.ymin.setMaximum(15000)
        self.ymin.setMinimum(0)
        self.ymin.setValue(0)
        self.ymin.setMaximumHeight(25)
        self.ymin.setMaximumWidth(100)
        
        #self.ymax = QTextEdit('2000')
        self.ymax = QSpinBox()
        self.ymax.setMaximum(15000)
        self.ymax.setMinimum(0)
        self.ymax.setValue(2000)
        self.ymax.setMaximumHeight(25)
        self.ymax.setMaximumWidth(100)
        
        self.xauto_label = QLabel('Auto?')
        self.xauto = QLabel('Auto?')
        
        self.xauto_label = QLabel('Auto?')
        self.xauto_box = QCheckBox()
        self.xauto_box.setChecked(True)
        
        self.yauto_label = QLabel('Auto?')
        self.yauto_box = QCheckBox()
        self.yauto_box.setChecked(True)
    
    def build_layout(self):

        self._layout = QGridLayout()
        self._layout.addWidget(self.limitlabel,0,0)
        
        self._layout.addWidget(self.minlabel,0,1)
        self._layout.addWidget(self.maxlabel,0,2)
    
        self._layout.addWidget(self.x_axis,1,0)
        self._layout.addWidget(self.xmin,1,1)
        self._layout.addWidget(self.xmax,1,2)
        self._layout.addWidget(self.xauto_label,1,3)
        self._layout.addWidget(self.xauto_box,1,4)
        
        
        self._layout.addWidget(self.y_axis,2,0)
        self._layout.addWidget(self.ymin,2,1)
        self._layout.addWidget(self.ymax,2,2)
        self._layout.addWidget(self.yauto_label,2,3)
        self._layout.addWidget(self.yauto_box,2,4)
        
        self.setLayout(self._layout)
        

class PressureWidget(QGroupBox):
    
    def __init__(self,title='Pressure Calibration'):
        
        super(PressureWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
    def build_widgets(self):
        
        self.firstpeak_label = QLabel('First peak')
        self.secondpeak_label = QLabel('Second peak')
        
        self.reference_label = QLabel('Reference')
        self.measured_label = QLabel('Current')
        
        self.firstpeak_reference = QTextEdit('693.7')
        self.firstpeak_reference.setMaximumHeight(25)
        self.firstpeak_reference.setMaximumWidth(60)
        
        self.firstpeak_value = QTextEdit('693.7')
        self.firstpeak_value.setMaximumHeight(25)
        self.firstpeak_value.setMaximumWidth(60)
                
        self.secondpeak_reference = QTextEdit('694.3')
        self.secondpeak_reference.setMaximumHeight(25)
        self.secondpeak_reference.setMaximumWidth(60)
        
        self.secondpeak_value = QTextEdit('694.3')
        self.secondpeak_value.setMaximumHeight(25)
        self.secondpeak_value.setMaximumWidth(60)
        
        self.temperature_label = QLabel('Temp. (K):')
        
        self.temperature_reference = QTextEdit('300')
        self.temperature_reference.setMaximumHeight(25)
        self.temperature_reference.setMaximumWidth(50)
        
        self.temperature_value = QTextEdit('300')
        self.temperature_value.setMaximumHeight(25)
        self.temperature_value.setMaximumWidth(50)

        self.fit_button = QPushButton('Fit')
        
        self.temperature_button = QPushButton('Estimate Temp.')
        
        self.pressure_button = QPushButton('Calc. Pressure')
        
        
        self.pressure_reference = QComboBox()
        self.pressure_reference.addItems(['Dewaele et al. 2008',
                                          'Mao et al. 1993'])
    
        self.print_pressure = QLabel('')
        self.print_pressure.setStyleSheet('color: red')
        self.print_pressure.setFont(QFont("Times",30,QFont.Bold))
        self.print_pressure.setAlignment(Qt.AlignCenter)
        
    def build_layout(self):

        self._layout = QVBoxLayout()
        
        self._peaks_layout = QGridLayout()
        
        
        self._peaks_layout.addWidget(self.reference_label,0,1)
        self._peaks_layout.addWidget(self.measured_label,0,2)
        
        self._peaks_layout.addWidget(self.firstpeak_label,1,0)
        self._peaks_layout.addWidget(self.firstpeak_reference,1,1)
        self._peaks_layout.addWidget(self.firstpeak_value,1,2)
        
        self._peaks_layout.addWidget(self.secondpeak_label,2,0)
        self._peaks_layout.addWidget(self.secondpeak_reference,2,1)
        self._peaks_layout.addWidget(self.secondpeak_value,2,2)
        
        self._peaks_layout.addWidget(self.temperature_label,3,0)
        self._peaks_layout.addWidget(self.temperature_reference,3,1)
        self._peaks_layout.addWidget(self.temperature_value,3,2)
        
        self._extras_layout = QHBoxLayout()        
        self._extras_layout.addWidget(self.fit_button)
        self._extras_layout.addWidget(self.pressure_reference)
            
        self._buttons_layout = QHBoxLayout()        
        self._buttons_layout.addWidget(self.temperature_button)
        self._buttons_layout.addWidget(self.pressure_button)
            
        self._layout.addLayout(self._peaks_layout)
        self._layout.addLayout(self._extras_layout)
        self._layout.addLayout(self._buttons_layout)
    
        self._layout.addWidget(self.print_pressure)
        
        self.setLayout(self._layout)
        

if __name__ == '__main__':
    app = QApplication([])
    widget = OptionsWidget(parent=None)
    widget.show()
    app.exec_()
