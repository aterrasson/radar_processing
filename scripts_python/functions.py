#
# coding: utf-8
#
# In[3]:
#
#-------------------------------------------------
# to install images2gif modules:
# conda install -c pingucarsti images2gif=1.0.1
#-------------------------------------------------
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
import images2gif
from PIL import Image, ImageDraw
import os
import sys
import random
import argparse
import webbrowser
#



def plot_bolton_bom(myradar,tilt1,tilt2,check_reflec=False):
    
    display = pyart.graph.RadarMapDisplay(myradar)
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    #outloc = '../plots/' 
    tz=11


    #---------------------------------------
    # Range of the plot
    #---------------------------------------
    #                                         East        South     West       North 
    min_lon, min_lat, max_lon, max_lat = [149.2767,-32.5433,151.1526,-31.4764]
    #min_lon, min_lat, max_lon, max_lat = [149.2767,-32.5433,151.1526,-30.4764]
    lat_lines = np.arange(np.ceil(max_lat),np.floor(min_lat),-.2)
    lon_lines = np.arange(np.floor(min_lon),np.ceil(max_lon),.2)
    contour_levels=np.arange(10,50,10)
 
    font = {'size': 7}
    matplotlib.rc('font', **font)
    f = plt.figure(figsize = [10,15])

    #---------------------------------------
    # Set plot parameters for reflectivty or velocity
    # By default velocity will be plot with reflectivity contour lines. If check_reflec is given True, then reflectivity is plot along with reflectivity contourlines.
    #---------------------------------------
    #plot of velocity
    if check_reflec==False:
        [outloc,field,vmin,vmax,colorbar_label,cmap,reference]=['../plots/Dop_velocity/','VRADH',-15,15,'Doppler Velocity (m/s)',pyart.graph.cm.BuDOr12,'Dop_Velocity']
    #plot of reflectivity to verify the contourlines
    elif check_reflec==True:
        [outloc,field,vmin,vmax,colorbar_label,cmap,reference]=['../plots/reflectivity/','DBZH',0,50,'Reflectivity (dBZ)',None,'Reflectivity']

    #---------------------------------------
    #creating the outloc directory if it doesn't exist
    #---------------------------------------
    if not os.path.exists(outloc): os.makedirs(outloc)
        

    #---------------------------------------            
    # Subplot 1: plot for sweep nb titl1
    #---------------------------------------    
    ax1=f.add_subplot(2,1,1)
    
    
    # ref_m = Basemap(llcrnrlon=min_lon,
    #             llcrnrlat=min_lat,
    #             urcrnrlon=max_lon,
    #             urcrnrlat=max_lat, 
    #             projection='tmerc', 
    #             resolution = 'i',
    #             epsg = GDA94)
    #m.arcgisimage(service= esriMap, xpixels = 1500, verbose= True)
    
    #load background image
    # im = plt.imread('/home/fuego/Desktop/SirIvanFire/basemap.png')
    # ref_m.imshow(im,zorder = 0,origin='upper')

    #---------------------------------------
    # plotting the chosen field
    #---------------------------------------
    display.plot_ppi_map(
        field,tilt1, vmin=vmin, vmax=vmax,
        lat_lines = lat_lines, lon_lines = lon_lines,
        max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
        title_flag=False,
        mask_outside = True,
        colorbar_label=colorbar_label,
        cmap = cmap,
        # basemap = ref_m,
        ax=ax1
        )
    display.plot_point(lon=myradar.longitude['data'][0],lat=myradar.latitude['data'][0],ax=ax1)

    #---------------------------------------
    # adding reflectivity contours
    #---------------------------------------
    
    #find raw ppi data start/stop index
    start = myradar.get_start(tilt1)
    end   = myradar.get_end(tilt1) + 1
    #load ppi data
    data  = myradar.fields['DBZH']['data'][start:end]
    #apply guassian smoothing
    data  = spyi.gaussian_filter(data, sigma=1.2)

    #load gat lat/lon grids
    lon = myradar.gate_longitude['data'][start:end]
    lat = myradar.gate_latitude['data'][start:end]

    #convert lat,lon to basemap coords
    x,y = display.basemap(lon,lat)
    

    #plot contours
    contours=ax1.contour(x,y,data,contour_levels,colors='k',linewidths=1)
    plt.clabel(contours,contour_levels,fmt='%r',inline=True,fontsize=10)

    #---------------------------------------
    #extract title parameters
    #---------------------------------------
    el1 = myradar.get_elevation(tilt1)
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
    scantime = dts[0].strftime('%H:%M Local Time on %Y %m %d')
    ax1.set_title('Sir Ivan Bushfire at {} at elevation {} degrees, {}'.format(scantime,el1[0],reference))

    #---------------------------------------
    # Subplot 2: plot for sweep nb titl2
    #---------------------------------------
    ax2=f.add_subplot(2,1,2)
    
    
    # ref_m = Basemap(llcrnrlon=min_lon,
    #             llcrnrlat=min_lat,
    #             urcrnrlon=max_lon,
    #             urcrnrlat=max_lat, 
    #             projection='tmerc', 
    #             resolution = 'i',
    #             epsg = GDA94)
    #m.arcgisimage(service= esriMap, xpixels = 1500, verbose= True)
    
    #load background image
    # im = plt.imread('/home/fuego/Desktop/SirIvanFire/basemap.png')
    # ref_m.imshow(im,zorder = 0,origin='upper')
    
    
    display.plot_ppi_map(
        field,tilt2, vmin=vmin, vmax=vmax,
        lat_lines = lat_lines, lon_lines = lon_lines,
        max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
        title_flag=False,
        mask_outside = True,
        colorbar_label=colorbar_label,
        cmap = cmap,
        # basemap = ref_m,
        ax=ax2
        )
    display.plot_point(lon=myradar.longitude['data'][0],lat=myradar.latitude['data'][0],ax=ax2)


    # add contours
    
    #find raw ppi data start/stop index
    start = myradar.get_start(tilt2)
    end   = myradar.get_end(tilt2) + 1
    #load ppi data
    data  = myradar.fields['DBZH']['data'][start:end]
    #apply guassian smoothing
    data  = spyi.gaussian_filter(data, sigma=1.2)

    #load gat lat/lon grids
    lon = myradar.gate_longitude['data'][start:end]
    lat = myradar.gate_latitude['data'][start:end]

    #convert lat,lon to basemap coords
    x,y = display.basemap(lon,lat)
    

    #plot contours
    contours=ax2.contour(x,y,data,contour_levels,colors='k',linewidths=1)
    plt.clabel(contours,contour_levels,fmt='%r',inline=True,fontsize=10)

    #extract title parameters
    el2 = myradar.get_elevation(tilt2)
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
    scantime = dts[0].strftime('%H:%M Local Time on %Y %m %d')
    ax2.set_title('Sir Ivan Bushfire at {} at elevation {} degrees, {}'.format(scantime,el2[0],reference))

 
    #---------------------------------------
    #Save the plot in outloc directory
    #---------------------------------------
    plt.savefig('{}Namoi_at_{}_el_{}_and{}_{}.png'.format(outloc,dts[0].strftime('%H%M_Z_on_%Y_%m_%d'),str(el1[0]),str(el2[0]),reference),dpi=400)
    
    #print('{}Namoi_at_{}_el_{}_and{}_{}.png'.format(outloc,dts[0].strftime('%H%M_Z_on_%Y_%m_%d'),str(el1[0]),str(el2[0]),reference ) )
    #plt.show()


    #print(m)
    
    plt.close()
    
    return


def makeAnimatedGif(path,name):
    # Recursively list image files and store them in a variable
    #path = "./Images/"
    os.chdir(path)
    # images=os.listdir()
    # images.sort()
    # for i in images:
    #     print(i)
    imfiles = sorted((fn for fn in os.listdir() if fn.endswith('.png')))
    print(imfiles)
    # Grab the images and open them all for editing
    im = [Image.open(fn) for fn in imfiles]

    filename = name + ".gif"
    images2gif.writeGif(filename, im, duration=0.1)
    #print(os.path.realpath(filename))
    #print("%s has been created, I will now attempt to open your" % filename)


