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
#
dirname = '/media/dossier_windows/Documents and Settings/ASUS/Mes documents/cesure aus/Sir_ivan_data/NamoiData/'
fls = os.listdir(dirname)
fls.sort()
#
#for c,i in enumerate(fls):
#    print(i)
#print(c)
outloc = '/media/dossier_windows/Documents and Settings/ASUS/Mes documents/cesure aus/Sir_ivan_data/plots'
#
#creating a radar object from the specified file
myrad=pyart.aux_io.read_odim_h5(
    dirname + fls[0],
    file_field_names=True
)
display=pyart.graph.RadarMapDisplay(myrad)
#
#setting the intervals of lat and lon for the plot
lat_width=1
lon_width=1
grid_step=0.25
#
min_la=np.floor(myrad.latitude['data'][0])-0.5*lat_width
max_la=np.ceil(myrad.latitude['data'][0])+0.5*lat_width
min_lo=np.floor(myrad.longitude['data'][0])-0.5*lon_width
max_lo=np.ceil(myrad.longitude['data'][0])+0.5*lon_width
#
lon_l=np.arange(min_lo,max_lo,grid_step)
lat_l=np.arange(min_la,max_la,grid_step)
#
print('min_lat={}, max_lat={}, min_lon={}, max_lon={}\n'.format(min_la, max_la, min_lo, max_lo ))
#
#plotting the total power filed (=equivalent reflectivity factor)

#choosing a field to plot (use of MDV code)
field='VRADH'
#field='DBZH'
if field=='VRADH':
    [vmi,vma,label]=[-15,15,'Doppler Velocity (m/s)']
elif field=='DBZH':
    [vmi,vma,label]=[0,40,'Reflectivity (dBZ)']

# plot options
display.plot_ppi_map(
    field=field,
    sweep=1,
    vmin=vmi,
    vmax=vma,
    min_lon=min_lo,
    min_lat=min_la,
    max_lon=max_lo,
    max_lat=max_la,
    lon_lines=lon_l,
    lat_lines=lat_l,
    mask_outside=True,
    colorbar_label=label,
    cmap=pyart.graph.cm.LangRainbow12
)
#
#ploting the radar position
display.plot_point(myrad.longitude['data'][0],myrad.latitude['data'][0])

#plotting some range rings
max_ring=100
nb_ring=4
for i in np.arange( 0 , max_ring , max_ring/nb_ring ):
    display.plot_range_ring(i,line_style='k-')


plt.show()
#
#
#
#
# In[5]
#getting the elevation and the azimuths of each sweep for a given file
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[0])
# print(myrad.nsweeps)
# for i in range(myrad.nsweeps):
#     print('sweep number {}.'.format(i))
#     print('elevation associated : {}'.format(myrad.get_elevation(i)[0]))
#     print('azimuth associated : {}\n\n'.format(myrad.get_azimuth(i)))
#
# In[6]
#getting the time associated with the sweeps 
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[0])
# print('lenght: {}'.format(len(myrad.time['data']) ) )
# for i in myrad.time.items():
#     print(i)
#
# In[7]
#
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[0])
# for f in myrad.fields.items():
#     print(f)


