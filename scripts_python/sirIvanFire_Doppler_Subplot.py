
# coding: utf-8

# In[3]:

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


# In[4]:

dirname = '/home/fuego/Desktop/SirIvanFire/NamoiData/'
fls = os.listdir(dirname)
fls.sort()
#print(fls[100])
outloc = '/home/fuego/Desktop/SirIvanFire/DopplerPlots/'


# In[5]:

rad = pyart.aux_io.read_odim_h5(dirname + fls[0], file_field_names=True)
radarlat = rad.latitude['data'][0]
radarlon = rad.longitude['data'][0]
del rad


# In[6]:

##### Lat/Lon bounds for PPIs

# Use the tool http://boundingbox.klokantech.com/ to output in correct format

#                                         East        South     West       North 
min_lon, min_lat, max_lon, max_lat = [149.2767,-32.5433,151.1526,-31.4764]

lat_lines = np.arange(np.ceil(max_lat),np.floor(min_lat),-.2)
lon_lines = np.arange(np.floor(min_lon),np.ceil(max_lon),.2)

rhi_azi = 299

xpol_lat = -27.888524
xpol_lon = 153.207886

tz = 11


# In[7]:

# epsg code for GDA94 Projection
GDA94 = 3112
    
# ArcGIS Online Map Service to use (e.g. World_Topo_Map or ESRI_Imagery_World_2D)
esriMap = 'World_Topo_Map'

m = Basemap(llcrnrlon=min_lon,
                llcrnrlat=min_lat,
                urcrnrlon=max_lon,
                urcrnrlat=max_lat, 
                projection='tmerc', 
                resolution = 'i',
                epsg = GDA94)
#m.arcgisimage(service= esriMap, xpixels = 1500, verbose= True)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[47]:

def plot_bolton_bom(myradar,tilt1,tilt2):
    display = pyart.graph.RadarMapDisplay(myradar)
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    
        
    font = {'size': 7}
    matplotlib.rc('font', **font)
    f = plt.figure(figsize = [6,5])
    
    # Subplot 1
    
    plt.subplot(2,1,1)
    
    
    ref_m = Basemap(llcrnrlon=min_lon,
                llcrnrlat=min_lat,
                urcrnrlon=max_lon,
                urcrnrlat=max_lat, 
                projection='tmerc', 
                resolution = 'i',
                epsg = GDA94)
    #m.arcgisimage(service= esriMap, xpixels = 1500, verbose= True)
    
    #load background image
    im = plt.imread('/home/fuego/Desktop/SirIvanFire/basemap.png')
    ref_m.imshow(im,zorder = 0,origin='upper')
    
    
    display.plot_ppi_map(
                        'VRADH',tilt1, vmin=-15, vmax=15,
                        #'DBZH',0, vmin=0, vmax=50, 
                        #lat_lines = lat_lines, lon_lines = lon_lines,
                        #max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
                        title_flag=False,
                        mask_outside = True,
                        colorbar_label='Doppler Velocity (m/s)',
                        cmap = pyart.graph.cm.BuDRd18,
                        basemap = ref_m,
                        zorder = 1,
                        )
    
    
    # add contours
    
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
    
    ax = plt.gca()
    
    #plot contours
    contours = ax.contour(x, y, data, [10,20], linewidths=0.3, colors='0.4',
                          linestyles='-', antialiased=True)
    contours = ax.contour(x, y, data, [25,30], linewidths=0.5, colors='0.25',
                          linestyles='-', antialiased=True)
    contours = ax.contour(x, y, data, [35], linewidths=1, colors='k',
                          linestyles='-', antialiased=True)
    
    #plt.clabel(contours, [35], fmt='%r', inline=True, fontsize=5)
    
    el1 = myradar.get_elevation(tilt1)

   
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
    scantime = dts[0].strftime('%H:%M Local Time on %Y %m %d')
    f.text(0.125, 0.92,'Sir Ivan Bushfire at ' + scantime + ' at elevation ' 
           + str(el1[0]) + ' degrees')
    
    # Subplot 2
    
    plt.subplot(2,1,2)
        
    ref_m = Basemap(llcrnrlon=min_lon,
                llcrnrlat=min_lat,
                urcrnrlon=max_lon,
                urcrnrlat=max_lat, 
                projection='tmerc', 
                resolution = 'i',
                epsg = GDA94)
    #m.arcgisimage(service= esriMap, xpixels = 1500, verbose= True)
    
    #load background image
    im = plt.imread('/home/fuego/Desktop/SirIvanFire/basemap.png')
    ref_m.imshow(im,zorder = 0,origin='upper')
    
   
    display.plot_ppi_map(
                        'VRADH',tilt2, vmin=-15, vmax=15,
                        #'DBZH',0, vmin=0, vmax=50, 
                        #lat_lines = lat_lines, lon_lines = lon_lines,
                        #max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
                        title_flag=False,
                        mask_outside = True,
                        colorbar_label='Doppler Velocity (m/s)',
                        cmap = pyart.graph.cm.BuDRd18,
                        basemap = ref_m,
                        zorder = 1,
                        )
    
    
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
    
    ax = plt.gca()
    
    #plot contours
    contours = ax.contour(x, y, data, [10,20], linewidths=0.3, colors='0.4',
                          linestyles='-', antialiased=True)
    plt.clabel(contours, [10,20], fmt='%r', inline=True, fontsize=3)
    contours = ax.contour(x, y, data, [25,30], linewidths=0.5, colors='0.25',
                          linestyles='-', antialiased=True)
    contours = ax.contour(x, y, data, [35], linewidths=1, colors='k',
                          linestyles='-', antialiased=True)
    
    plt.clabel(contours, [35], fmt='%r', inline=True, fontsize=5)
    
    el2 = myradar.get_elevation(tilt2)

   
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
    scantime = dts[0].strftime('%H:%M Local Time on %Y %m %d')
    f.text(0.125, 0.5,'Sir Ivan Bushfire at ' + scantime + ' at elevation ' 
           + str(el2[0]) + ' degrees')
    
    
    
    

    plt.savefig(outloc + 'Namoi_at_' + (dts[0].strftime('%H%M_Z_on_%Y_%m_%d')) + 'el_'
               + str(el1[0]) + '_and_' + str(el2[0]) + '_Dop.png', dpi=400)

    #print(m)
    
    plt.close()
    
    return


# In[48]:

plot_bolton_bom(myradar,0,3)


# In[38]:

myradar = pyart.aux_io.read_odim_h5(dirname + fls[40], file_field_names=True)
vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
print(vol_t)


# In[10]:

plt.close()


# In[36]:

i = 0
for fl in fls:
    #print('Doing scan number ' + str(i+1))
    myradar = pyart.aux_io.read_odim_h5(dirname + fl, file_field_names=True)
    plot_bolton_bom(myradar,0,3)
    i = i + 1
print('Finished, completed ' + str(i+1) + ' scans')


# In[13]:

tz = 11.
#dts = myradar.time['data'] + tz*60.*60.
dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
datestr = dts[0].strftime('%H:%M Local on %Y-%m-%d')
datestr


# In[24]:


    # add a title
    slc_height = round(grid.z['data'][level])
    dateval = grid.time['data'] + 8.*60.*60.
    # print(grid.time['data'])
    dts = num2date(dateval, grid.time['units'])
    datestr = dts[0].strftime('%H:%M Z on %Y-%m-%d')
    title = 'Sliced at ' + str(slc_height) + ' meters at ' + datestr
    fig.text(0.5, 0.9, title)

    fn = (dts[0].strftime('%H:%M_Z_on_%Y_%m_%d'))
    plt.savefig(outloc + 'Slice_plot_WyeRiver_Fire_at_' + fn + '_Refl.png', dpi=100)
    plt.close()



    ## Repeat for Doppler

    # create the figure
    font = {'size': 16}
    matplotlib.rc('font', **font)
    fig = plt.figure(figsize=[15, 8])

    # panel sizes
    map_panel_axes = [0.05, 0.05, .4, .80]
    x_cut_panel_axes = [0.55, 0.10, .4, .30]
    y_cut_panel_axes = [0.55, 0.50, .4, .30]
    colorbar_panel_axes = [0.05, 0.90, .4, .03]

    # parameters
    level = 5


    # panel 1, basemap, radar reflectivity and NARR overlay
    ax1 = fig.add_axes(map_panel_axes)
    display.plot_basemap()
    display.plot_grid('VRADH', level=level, vmin=vminrad, vmax=vmaxrad, title_flag=False,
                      colorbar_flag=False,
                      cmap = pyart.graph.cm.NWSVel,
                     )
    display.plot_crosshairs(lon=lon, lat=lat)
    


# In[15]:

#grid = regrid(myradar)


# In[25]:

#plotgrids(grid)


# In[53]:

#pyart.io.write_grid('/media/fuego/Seagate Expansion Drive/WaroonaFire_netcdf/radar' + fls[50][:-3] + '.nc', grid)


# In[42]:




# In[ ]:




# In[ ]:



