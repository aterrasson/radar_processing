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
from functions import *
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
x_rad,yrad=display.basemap(myradar.longitude['data'][0],myradar.latitude['data'][0])

print(x_rad,y_rad)
