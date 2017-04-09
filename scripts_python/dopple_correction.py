#
# coding: utf-8
#
# In[3]:
#
#imports
from __future__ import print_function
import pyart
import matplotlib.pyplot as plt
import matplotlib
#%matplotlib inline
import numpy as np
import os
from scipy import ndimage, signal
import scipy.ndimage as spyi
from netCDF4 import num2date, date2num
import datetime as dt
from mpl_toolkits.basemap import Basemap
#
#
# In[4]:
#-------------------------------------------------
#setting the data directory, the data files and
#the output directory
#-------------------------------------------------
dirname = '/media/dossier_windows/Documents and Settings/ASUS/Mes documents/cesure aus/Sir_ivan_data/NamoiData/'
fls = os.listdir(dirname)
fls.sort()
#
#for c,i in enumerate(fls):
#    print(i)
#print(c)
outloc = '/media/dossier_windows/Documents and Settings/ASUS/Mes documents/cesure aus/Sir_ivan_data/plots/'
#
#-------------------------------------------------
#creating a radar object from the specified file
#-------------------------------------------------
myrad=pyart.aux_io.read_odim_h5(
    dirname + fls[0],
    file_field_names=True
)
display=pyart.graph.RadarDisplay(myrad)
#
#-------------------------------------------------
#smoothering reflectivity
#-------------------------------------------------
#
sigma=1.2
C_DBZH=pyart.correct.despeckle._smooth_data(myrad.fields['DBZH'],3)
myrad.add_field('C_DBZH',C_DBZH)
#
#-------------------------------------------------
#setting the intervals of lat and lon for the plot
#-------------------------------------------------
#
#
#-------------------------------------------------
#PLOTTING
#-------------------------------------------------
sweep=0
#
plt.close()
fig=plt.figure(figsize=(15,6))
[vmi,vma,label]=[-30,30,'Doppler Velocity (m/s)']
#first subplot: non corrected sweep1
ax1=fig.add_subplot(1,2,1)
display.plot(
    field='VRADH',
    sweep=sweep,
    vmin=vmi,
    vmax=vma,
    mask_outside=True,
    colorbar_label=label,
    cmap=pyart.graph.cm.LangRainbow12
#    axislabels=('W-E distance from the radar (km)','N-S distance from radar (km)')
)
display.plot_range_rings([10,100],lw=1)
display.plot_cross_hair(5)
display.set_limits((-100,100),(-100,100))
display.plot_grid_lines(col='k',ls='--')

[vmi,vma,label]=[0,30,'Raw reflectivity (dBZ)']
ax2=fig.add_subplot(1,2,2)
display.plot(
    field='DBZH',
    sweep=sweep,
    vmin=vmi,
    vmax=vma,
    mask_outside=True,
    colorbar_label=label,
    cmap=pyart.graph.cm.LangRainbow12
#    axislabels=('W-E distance from the radar (km)','N-S distance from radar (km)')
)
display.plot_range_rings([10,100],lw=1)
display.plot_cross_hair(5)
display.set_limits((-100,100),(-100,100))
display.plot_grid_lines(col='k',ls='--')

#
#
plt.show()

