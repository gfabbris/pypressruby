'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np

from scipy.optimize import curve_fit

def make_dummy(x,
               amplitude1=100,sigma1=0.5,x01=695,constant1=1,
               amplitude2=200,sigma2=0.5,x02=696.5,constant2=1):

    gauss  = gaussian(x,amplitude1,sigma1,x01,constant1)
    gauss += gaussian(x,amplitude2,sigma2,x02,constant2)
    
    return gauss
    
def gaussian(x,amplitude,sigma,x0,constant):
    return amplitude/sigma/np.sqrt(2*np.pi)*np.exp(-(x-x0)**2/2/sigma**2)+constant

def two_gaussians(x,amplitude1,sigma1,x01,
                    amplitude2,sigma2,x02,constant):
    
    y = gaussian(x,amplitude1,sigma1,x01,constant)
    y += gaussian(x,amplitude2,sigma2,x02,constant)
    
    return y

def fit_data(xoriginal,y,xmin=None,xmax=None):

    if y is None:
        return 'No spectrum! Fit not performed!'
    else:
        
        if xmin is None:
            xmin = xoriginal.min()
        elif xmin < xoriginal.min():
            xmin = xoriginal.min()
        
        if xmax is None:
            xmax = xoriginal.max()
        elif xmax < xoriginal.max():
            xmax = xoriginal.max()
        
        x = xoriginal[np.logical_and(xoriginal>xmin,xoriginal<xmax)]
        y = y[np.logical_and(xoriginal>xmin,xoriginal<xmax)]
        
        x01 = x[y==y.max()]
        sigma1 = 0.5
        amplitude1 = y.max()*sigma1*np.sqrt(2*np.pi)
        
        x02 = x01-0.7
        sigma2 = 0.5
        amplitude2 = amplitude1/2.
        
        constant = y.min()

        p0 = [amplitude1,sigma1,x01,amplitude2,sigma2,x02,constant]
        
        try:
            pfit,pcov = curve_fit(two_gaussians,x,y,p0=p0)
            return pfit
        except RuntimeError:
            return 'Fit failed! Try changing initial parameters.'

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
