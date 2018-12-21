        
    def start_spectrometer_old(self):
        
        if self.spec is not None:
            
            self.integration_time = float(self.spectrometer.integrate.toPlainText())
            
            self.stop_signal = 1
            graph = None
            
            self.plot.figure.clear()
            self.ax = self.plot.figure.add_subplot(111)
            
            self.plot.canvas.draw()
            self.plot.canvas.flush_events()
            time.sleep(0.0001)
            
            x,gauss = self.make_dummy()

            while self.stop_signal != 0:
                    
                self.spec.integration_time_micros(1E3*self.integration_time)
                self.y = self.spec.intensities()
                
                #time.sleep(self.integration_time/1000.)
                #self.y = gauss + np.random.rand(gauss.size)*10
                
                if self.spectrometer.dark_box.isChecked():
                    if self.dark is not None:
                        self.y -= self.dark
                        self.status.showMessage('Ready')
                    else:
                        self.status.showMessage('Dark image has not been collected!!')
                
                if graph is None:
                    self.x = self.spec.wavelengths()
                    #self.x = x
                    graph = self.ax.plot(self.x,self.y,color='black')[0]
                else:
                    graph.set_ydata(self.y)
                
                
                autoy = self.graph.yauto_box.isChecked()
                if autoy:
                    self.update_ylimit()
                else:
                    self.update_ylimit(limits=[float(self.graph.ymin.toPlainText()),
                                               float(self.graph.ymax.toPlainText())])
    
                autox = self.graph.xauto_box.isChecked()
                if autox:
                    self.update_xlimit()
                else:
                    self.update_xlimit(limits=[float(self.graph.xmin.toPlainText()),
                                               float(self.graph.xmax.toPlainText())])
               
                self.plot.canvas.draw()
                self.plot.canvas.flush_events()
                time.sleep(0.0001)
                
        else:
            self.status.showMessage('Spectrometer is not loaded!')
            
            
            

    def collect_signal(self):
        
        if self.stop_signal != 0:
            self.stop_spectrometer
        
        if self.spec is not None:
            
            self.integration_time = float(self.spectrometer.integrate.toPlainText())
            
            self.stop_signal = 1
            graph = None
            
            self.plot.figure.clear()
            self.ax = self.plot.figure.add_subplot(111)

            self.spec.integration_time_micros(1E3*self.integration_time)
            
            self.x = self.spec.wavelengths()
            self.y = self.spec.intensities()
            
            thread.start_new_thread(self.start_spectrometer,())

            while self.stop_signal != 0:
                
                if graph is None:
                    graph = self.ax.plot(self.x,self.y,color='black')[0]
                else:
                    graph.set_ydata(self.y)

                autoy = self.graph.yauto_box.isChecked()
                if autoy:
                    self.update_ylimit()
                else:
                    try:
                        ymin = float(self.graph.ymin.toPlainText())
                    except ValueError:
                        ymin = self.y.min()
                    try:
                        ymax = float(self.graph.ymax.toPlainText())
                    except ValueError:
                        ymax = self.y.max()
                    
                    self.update_ylimit(limits=[ymin,ymax])
    
                autox = self.graph.xauto_box.isChecked()
                if autox:
                    self.update_xlimit()
                else:
                    try:
                        xmin = float(self.graph.xmin.toPlainText())
                    except ValueError:
                        xmin = self.x.min()
                    try:
                        xmax = float(self.graph.xmax.toPlainText())
                    except ValueError:
                        xmax = self.x.max()
                    self.update_xlimit(limits=[xmin,xmax])
                
                self.plot.canvas.draw()
                self.plot.canvas.flush_events()
                sleep(0.001)
                
        else:
            self.status.showMessage('Spectrometer is not loaded!')
    
    def start_spectrometer(self):
                    
        gauss = self.make_dummy()
        
        while self.stop_signal != 0:

            self.y = self.spec.intensities() + gauss
            
            if self.spectrometer.dark_box.isChecked():
                if self.dark is not None:
                    self.y -= self.dark
                    self.status.showMessage('Ready')
                else:
                    self.status.showMessage('Dark image has not been collected!!')
        
    def stop_spectrometer(self):  
        self.stop_signal = 0
        sleep(0.1)
    
    def update_xlimit(self,limits=None):
        if limits:
            self.ax.set_xlim(limits[0],limits[1])
        else:
            self.ax.set_xlim(self.x.min(),self.x.max())
    
    def update_ylimit(self,limits=None):
        if limits:
            self.ax.set_ylim(limits[0],limits[1])
        else:
            dy = (self.y.max()-self.y.min())*0.05
            self.ax.set_ylim(self.y.min()-dy,self.y.max()+dy)
            