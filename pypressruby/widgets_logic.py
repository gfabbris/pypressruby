'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

import seabreeze.spectrometers as sb
from PyQt5.QtCore import QObject
import numpy as np
from time import sleep
import _thread as thread
from pypressruby.logic import make_dummy,fit_data,two_gaussians,calculate_pressure

class LogicWidgets(QObject):
    def __init__(self,status,options,plot):
        
        super(LogicWidgets, self).__init__()
        
        self.status = status
        self.spectrometer = options.spectrometer
        self.graph = options.graph
        self.pressure = options.pressure
        self.plot = plot
        
        self.make_connections()
        
        self.spec = None
        self.dark = None
        self.y = None
        self.fit = None
        self.data_line = None
        self.vline = None
        self.stop_signal = 0
        self.timer = None
        self.integration_time = float(self.spectrometer.integrate.toPlainText())

        self.load_devices()
               
    def make_connections(self):
        
        self.spectrometer.start_button.clicked.connect(self.collect_signal)
        self.spectrometer.stop_button.clicked.connect(self.stop_spectrometer)
        
        self.spectrometer.reload_button.clicked.connect(self.load_devices)
        self.spectrometer.spec_name.activated[str].connect(self.update_spec)
        
        self.spectrometer.dark_button.clicked.connect(self.collect_dark)
        self.spectrometer.dark_box.stateChanged.connect(self.dark_msg)
        
        self.pressure.fit_button.clicked.connect(self.run_fit)   
        self.pressure.clearfit_button.clicked.connect(self.clear_fit)     
        self.pressure.pressure_button.clicked.connect(self.get_pressure)
        
        self.plot.canvas.mpl_connect('button_press_event', self.onclick)
        
        self.graph.xmin.valueChanged.connect(self.update_xlimit)
        self.graph.xmax.valueChanged.connect(self.update_xlimit)
        self.graph.xauto_box.stateChanged.connect(self.update_xlimit)
        
        self.graph.ymin.valueChanged.connect(self.update_ylimit)
        self.graph.ymax.valueChanged.connect(self.update_ylimit)
        self.graph.yauto_box.stateChanged.connect(self.update_ylimit)

    def load_devices(self):
        
        self.stop_signal = 0
        sleep(self.integration_time/1000.*1.1)
        
        self.devices = {}
        
        try:
            for device in sb.list_devices():
                self.devices[device.model] = device
        
            self.update_spec_list(self.devices.keys())
            self.update_spec(self.spectrometer.spec_name.currentText())
        except KeyError:
            self.status.showMessage('No spectrometer was found!')
            
            
    def update_spec_list(self,devices):
        self.spectrometer.spec_name.clear()
        self.spectrometer.spec_name.addItems(devices)
    
    def update_spec(self,text):
        try:
            self.spec.close()
        except AttributeError:
            pass
        
        self.spec = sb.Spectrometer(self.devices[text])

    def collect_signal(self):
        
        if self.stop_signal != 0:
            self.stop_spectrometer()
        
        if self.spec is not None:
            
            self.integration_time = float(self.spectrometer.integrate.toPlainText())
            self.spec.integration_time_micros(1E3*self.integration_time)
        
            self.stop_signal = 1
            
            self.x = self.spec.wavelengths()
            self.y = self.spec.intensities()
        
            self.start_figure()
            
            thread.start_new_thread(self.start_spectrometer,())
            
            self.status.showMessage('Ready!')
        else:
            self.status.showMessage('Spectrometer is not loaded!')
    
    def start_spectrometer(self):
                    
        #gauss = make_dummy(self.x)
        
        while self.stop_signal != 0:

            self.y = self.spec.intensities()# + gauss
            
            if self.spectrometer.dark_box.isChecked():
                if self.dark is not None:
                    self.y -= self.dark
        
    def stop_spectrometer(self):  
        self.stop_signal = 0
        sleep(self.integration_time*1.05/1000)
        if self.timer:
            self.timer.stop()
            self.timer = None
        
    def collect_dark(self):
        
        if self.stop_signal != 0:
            restart = True
            self.stop_spectrometer()
        else:
            restart = False
            self.integration_time = float(self.spectrometer.integrate.toPlainText())
            self.spec.integration_time_micros(1E3*self.integration_time)

        self.dark = self.spec.intensities()
        
        if restart is True:
            self.collect_signal()
        
        self.status.showMessage('Ready!')
            
    def dark_msg(self):
        if self.spectrometer.dark_box.isChecked():
            if self.dark is None:
                self.status.showMessage('Dark spectrum has not been collected!!')
        
    def start_figure(self):
        
        if self.data_line is None:
            self.plot.figure.clear()
            self.ax = self.plot.figure.add_subplot(111)
            
            self.ax.set_ylabel('Intensity')
            self.ax.set_xlabel('Wavelength (nm)')
            
            self.ax.tick_params(which='both',direction='in',right=True,top=True,
                                labelsize=8)
            
            self.data_line = self.ax.plot(self.x,self.y,color='black')[0]
            
        self.timer = self.plot.canvas.new_timer(10, [(self.update_canvas, (), {})])
        self.timer.start()
        
    def update_canvas(self):
        self.data_line.set_ydata(self.y)
        self.update_xlimit()
        self.update_ylimit()
        self.plot.canvas.draw()
        
    def update_xlimit(self):

        autox = self.graph.xauto_box.isChecked()
        if autox:
            dx = (self.x.max()-self.x.min())*0.05
            self.ax.set_xlim(self.x.min()-dx,self.x.max()+dx)  
        else:
            self.ax.set_xlim(self.graph.xmin.value(),self.graph.xmax.value())
            
        if self.timer is None:
            self.single_canvas_update()
            
    def update_ylimit(self):

        autoy = self.graph.yauto_box.isChecked()
        if autoy:
            if (self.y.min() == 0) & (self.y.max() == 0):
                self.ax.set_ylim(-1,1)
            else:
                dy = (self.y.max()-self.y.min())*0.05
                self.ax.set_ylim(self.y.min()-dy,self.y.max()+dy)  
        else:
            self.ax.set_ylim(self.graph.ymin.value(),self.graph.ymax.value())
        
        if self.timer is None:
            self.single_canvas_update()
    
    def run_fit(self):
        
        xmin,xmax = self.ax.get_xlim()
        result = fit_data(self.x,self.y,xmin=xmin,xmax=xmax)
        
        if type(result) is str:
            self.status.showMessage(result)
        else:
            if self.fit is not None:
                self.ax.lines.remove(self.fit)
                
            self.fit = self.ax.plot(self.x,two_gaussians(self.x,*result),color='red')[0]
            
            if result[2] < result[5]:
                first = result[2]
                second = result[5]
            else:
                first = result[5]
                second = result[2]
            
            
            self.plot_vline(second)
            self.pressure.firstpeak_value.setText('{:.2f}'.format(first))
            self.pressure.secondpeak_value.setText('{:.2f}'.format(second))
            
    def clear_fit(self):
        
        if self.fit is not None:
            self.ax.lines.remove(self.fit)
            
    def get_pressure(self):
        
        try:
            wavenumber = float(self.pressure.secondpeak_value.toPlainText())
            wavenumber_ref = float(self.pressure.secondpeak_reference.toPlainText())
            temperature = float(self.pressure.temperature_value.toPlainText())
            temperature_ref = float(self.pressure.temperature_reference.toPlainText())
            reference = self.pressure.pressure_reference.currentText()
            
            pressure = calculate_pressure(wavenumber,wavenumber_ref,temperature,temperature_ref,
                                          reference=reference)
            
            self.pressure.print_pressure.setText('P = {:.2f} GPa'.format(pressure))
            self.status.showMessage('Ready')
            
        except ValueError:
            self.status.showMessage('Pressure calculation failed!!!')
    
    def onclick(self,event):
        if self.ax:
            self.plot_vline(event.xdata)
            self.pressure.secondpeak_value.setText('{:.2f}'.format(event.xdata))
            
    def single_canvas_update(self):
        self.plot.canvas.draw()
        self.plot.canvas.flush_events()
            
    def plot_vline(self,x0):
        
        if self.vline:
            self.ax.lines.remove(self.vline)
        self.vline = self.ax.axvline(x=x0,ls='--',lw=1,color='blue')
        if self.timer is None:
            self.single_canvas_update()
                