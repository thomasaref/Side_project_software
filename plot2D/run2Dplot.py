# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 16:00:28 2014

@author: thomasaref
"""
import plot2D
reload(plot2D)
from plot2D import myImagePlot
from numpy import squeeze, transpose, shape, linspace, arange, mean
import h5py

#filename="/Users/thomasaref/Dropbox/Current stuff/sample3/digitizer/lt/sample3_digitizer_f_sweep_t_300mk_100nspulse.hdf5"

filename="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy5_2.hdf5"
filename="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy7.hdf5"
filename="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy16.hdf5"


with h5py.File(filename, 'r') as f:
    Magvec=f["Traces"]["Agilent VNA - S21"][:]
    yoko=f["Data"]["Data"][:]
    print f.attrs.keys(), f.attrs.values()
    #print f["Traces"].keys()
    #print 
    f0, fstep=squeeze(f["Traces"]['Agilent VNA - S21_t0dt'][:])
    #print f0, fstep
    l=shape(Magvec)[0]
    freq=linspace(f0, f0+fstep*(l-1), l)
#    freq=f
#    time=f["Traces"]["d - AvgTrace - t"][:]
#    Magvec=f["Traces"]["d - AvgTrace - Magvec"][:]
#    frequency=f["Data"]["Data"][:]
#    for name in f["Data"]:
#        print name


yoko=squeeze(yoko)    
#time=squeeze(time)

Magvec=squeeze(Magvec[:,0,:])
Magvec=Magvec-mean(Magvec, axis=1, keepdims=True)
#frequency=squeeze(frequency)

#x = time[:,0]*1.0e6
#y = frequency[0,:]/1.0e9
#z=transpose(Magvec*1000.0)
x = yoko[:]#*1.0e6
y = freq[:]/1.0e9
z=Magvec*1000.0
#
print shape(x)
print shape(y)
print shape(z)
ip=myImagePlot(x,y,z)
ip.configure_traits()
#
#ip=myImagePlot(x,y,z)
#ip.configure_traits()