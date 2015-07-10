A 2D image plot viewer in Python compatible with hdf5 files (e.g. data files from Simon's measurement software).

You need to run it in a python environment that has Enthought Tool Suites (ETS) installed, such as Anaconda or Canopy (it is not included in pythonxy). In Canopy, I had to set the "pylab backend" in "preferences" to "Interactive(wx)" to get it to work. You will also need h5py installed.

Everything that you should edit is in "run2Dplot.py". For example, you will have to change the filename to an appropriate one for your system and also the dataset names as appropriate. I attached a sample hdf5 file as an example. 

If you want to mess with how the plotting software itself actually works, you can edit "plot2D.py" but you will need to be fairly familiar with how Enthought's Traits, TraitsUI and Chaco packages work.



