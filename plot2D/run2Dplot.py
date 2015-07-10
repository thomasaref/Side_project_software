# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 16:00:28 2014

@author: thomasaref
"""
import plot2D
reload(plot2D)
from plot2D import myImagePlot
from numpy import squeeze, transpose
import h5py

filename="/Users/thomasaref/Dropbox/Current stuff/sample3/digitizer/lt/sample3_digitizer_f_sweep_t_300mk_100nspulse.hdf5"

with h5py.File(filename, 'r') as f:
    
    time=f["Traces"]["d - AvgTrace - t"][:]
    Magvec=f["Traces"]["d - AvgTrace - Magvec"][:]
    frequency=f["Data"]["Data"][:]
#    for name in f["Data"]:
#        print name
    
time=squeeze(time)
Magvec=squeeze(Magvec)
frequency=squeeze(frequency)

x = time[:,0]*1.0e6
y = frequency[0,:]/1.0e9
z=transpose(Magvec*1000.0)

ip=myImagePlot(x,y,z)
ip.configure_traits()