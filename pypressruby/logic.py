'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
from scipy.optimize import curve_fit
from lmfit.models import ConstantModel, PseudoVoigtModel

def make_dummy(x,amplitude1=100,sigma1=0.5,x01=695,constant1=1,
               amplitude2=200,sigma2=0.5,x02=696.5,constant2=1):

    gauss  = gaussian(x,amplitude1,sigma1,x01,constant1)
    gauss += gaussian(x,amplitude2,sigma2,x02,constant2)
    
    return gauss
    
def gaussian(x,amplitude,sigma,x0,constant):
    return amplitude/sigma/np.sqrt(2*np.pi)*np.exp(-(x-x0)**2/2/sigma**2)+constant

def remove_spike(y, x=None, nstd=2.):
    if x is None:
        x = np.arange(len(y))
    rj = np.sqrt((x[:-1] - x[1:])**2 + (y[:-1] - y[1:])**2)
    ind = rj > np.median(rj) + nstd*np.std(rj)
    spikes_ind = np.hstack(([True], ind[:-1] * ind[1:], [True])) 
    return (x[~spikes_ind], y[~spikes_ind])
    
    
        
def fit_data(x,y,xmin=None,xmax=None):
    
    if y is None:
        return 'No spectrum! Fit not performed!'
    else:
        
        if xmin is None:
            xmin = x.min()
        elif xmin < x.min():
            xmin = x.min()
        
        if xmax is None:
            xmax = x.max()
        elif xmax < x.max():
            xmax = x.max()
            
        y = np.copy(y[np.logical_and(x>xmin,x<xmax)])
        x = np.copy(x[np.logical_and(x>xmin,x<xmax)])
        
        x, y = remove_spike(y, x=x)
        
        mod = ConstantModel() + PseudoVoigtModel(prefix='peak1_') + PseudoVoigtModel(prefix='peak2_')
        params = mod.make_params()
        
        ymax_ind = np.argmax(y)
        xmax = x[ymax_ind]
        
        params['c'].set(0)
        params.add('psplit', value=1.5, vary=True, min=0.5, max=2.0)
        
        params['peak2_center'].set(xmax,min=xmax-0.5,max=x.max())
        params['peak2_sigma'].set(0.5,min=0.01)
        params['peak2_amplitude'].set(y[ymax_ind]*0.5*np.sqrt(2*np.pi),min=0)
        params['peak2_fraction'].set(0.5,min=0,max=1)

        params['peak1_center'].set(vary=False, expr='peak2_center-psplit')
        params['peak1_sigma'].set(0.5,min=0.01)
        params['peak1_amplitude'].set(y[ymax_ind]*0.5*np.sqrt(2*np.pi)/2,min=0)
        params['peak1_fraction'].set(0.5,min=0,max=1)
        
        
        fit = mod.fit(y,params,x=x)
        
        return fit
        

def calculate_pressure(wavenumber,wavenumber_ref,temperature,temperature_ref,
                       reference='Dewaele et al. 2008'):
    
    if reference == 'Mao et al. 1993':
        A = 1904
        B = 7.665
    else:
        A = 1920
        B = 9.61
        
    # Convert wavenumber to wavelength for T dependence
    wavelength_ref = 1E7/wavenumber_ref
    
    # Temperature parameters for R1 from Ragan et al. 1992
    a1 = 4.49E-2
    a2 = -4.81E-4
    a3 = 3.71E-7
    
    # Calculating a0 for the reference
    a0 = wavelength_ref - a1*temperature_ref - a2*temperature_ref**2 - a3*temperature_ref**3
    
    # Calculating the corrected wavelength for reference (if temperature is different)
    if np.abs(temperature-temperature_ref) > 0.5:
        wavelength_ref = a0 + a1*temperature + a2*temperature**2 + a3*temperature**3
        wavenumber_ref = 1E7/wavelength_ref
    
    return A/B*((wavenumber/wavenumber_ref)**B-1)
