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
#creating a radar object from the specified file
#then plotting the velocity and reflectivity contourlines
#-------------------------------------------------
# for c,i in enumerate(fls):
#     myrad=pyart.aux_io.read_odim_h5(
#         dirname + i,
#         file_field_names=True
#     )

#     plot_bolton_bom(myrad,0,3,True)
#     print('{} files processed over {}. {}% Done'.format(c+1,len(fls),(c+1)/len(fls)*100))

#-------------------------------------------------
#
#-------------------------------------------------
#makeAnimatedGif('../plots/Dop_velocity/','Doppler')
os.chdir('../plots/Dop_velocity/')
im=Image.open('Namoi_at_2330_Z_on_2017_02_12_el_0.5_and1.8_Dop_Velocity.png')
print(im.size)
im.save('Namoi_at_2330_Z_on_2017_02_12_el_0.5_and1.8_Dop_Velocity_72.png',dpi=72)
#im=[Image.open(fn) for fn in images]
#images2gif.writeGif('test1.gif',im,duration=0.1)
#os.system('convert *.png test.gif

#random change to test github
