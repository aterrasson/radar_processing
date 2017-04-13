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
dirname = '../NamoiData/'
fls = os.listdir(dirname)
fls.sort()
#
#for c,i in enumerate(fls):
#    print(i)
#print(c)
outloc = '../plots/'
#
#-------------------------------------------------
myrad=pyart.aux_io.odim_h5.read_odim_h5(dirname+fls[30],file_field_names=True)
plot_bolton_2_slices(myradar=myrad,sweep=0,azimuth=[170,197],field="VRADH",option='show')
# for k in myrad.fields.keys():
#     print(k)


