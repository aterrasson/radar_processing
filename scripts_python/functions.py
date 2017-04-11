#
# coding: utf-8
#
# In[3]:
#
#
#imports
from imports import *

    #---------------------------------------
    # Range of lat/lon for the plot
    #---------------------------------------
    #                                         East        South     West       North 
min_lon, min_lat, max_lon, max_lat = [149.2767,-32.5433,151.1526,-31.4764]
    #min_lon, min_lat, max_lon, max_lat = [149.2767,-32.5433,151.1526,-30.4764]
lat_lines = np.arange(np.ceil(max_lat),np.floor(min_lat),-.2)
lon_lines = np.arange(np.floor(min_lon),np.ceil(max_lon),.2)

def plot_bolton_bom(myradar,sweep,field,contour_field='DBZH',option='show'):
    
    display = pyart.graph.RadarMapDisplay(myradar)
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    #outloc = '../plots/' 
    tz=11
    el1 = myradar.get_elevation(sweep)[0]
    
    # contour level that will be plotted
    contour_levels=np.arange(10,50,10)
 
    font = {'size': 7}
    matplotlib.rc('font', **font)
    f = plt.figure(figsize=(10,5),dpi=100)

    #---------------------------------------
    # 
    #---------------------------------------
    #plot of velocity
    if field=='VRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/dop_velocity/angle_{}/'.format(el1),-15,15,'Doppler Velocity (m/s)',pyart.graph.cm.BuDOr12,'dop_Velocity']
        
    #plot of reflectivity
    elif field=='DBZH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/reflectivity/angle_{}/'.format(el1),0,50,'Reflectivity (dBZ)',None,'Reflectivity']
        
    #plot spec width
    elif field=='WRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/spec_width/angle_{}/'.format(el1),0,10,'Spec Width (m/s)',pyart.graph.cm.BuDOr12,'Spec_width']

    #---------------------------------------
    #creating the outloc directory if it doesn't exist
    #---------------------------------------
    if not os.path.exists(outloc): os.makedirs(outloc)
        
    #---------------------------------------            
    # creating the basemap
    #---------------------------------------    
    ax1=f.add_subplot(1,1,1)
    
    
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
        field=field,sweep=sweep, vmin=vmin, vmax=vmax,
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
    start = myradar.get_start(sweep)
    end   = myradar.get_end(sweep) + 1
    #load ppi data
    data  = myradar.fields[contour_field]['data'][start:end]
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
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])
    scantime = dts[0].strftime('%H:%M Local Time on %Y %m %d')
    ax1.set_title('Sir Ivan Bushfire at {} at elevation {} degrees, {}'.format(scantime,el1,reference) )
    ax1.text(x=0.1,y=0.9,s='t={}'.format(dts[0].strftime('%H%M')),fontsize=20,transform=ax1.transAxes )
    #---------------------------------------
    #Save the plot in outloc directory
    #---------------------------------------
    if option=='save':
        plt.savefig('{}Namoi_at_{}_el_{}_{}.png'.format(outloc,dts[0].strftime('%H%M_Z_on_%Y_%m_%d'),str(el1),reference),dpi=100)
    if option=='show':
        plt.show()

        
    #print(m)
    
    plt.close()
    
    return

def plot_bolton_1_slice(myradar,sweep,field,start_point=[0,0],azimuth=0,option='show'):
    
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    #outloc = '../plots/' 
    tz=11
    el1 = myradar.get_elevation(sweep)[0]


    #-------------------------------------------------
    #specifying the field parameters
    #-------------------------------------------------
    #plot of velocity
    if field=='VRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/dop_velocity/angle_{}/'.format(el1),-15,15,'Doppler Velocity (m/s)',pyart.graph.cm.BuDOr12,'dop_Velocity']
        
    #plot of reflectivity
    elif field=='DBZH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/reflectivity/angle_{}/'.format(el1),0,50,'Reflectivity (dBZ)',None,'Reflectivity']
        
    #plot spec width
    elif field=='WRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/spec_width/angle_{}/'.format(el1),0,10,'Spec Width (m/s)',pyart.graph.cm.BuDOr12,'Spec_width']
        
    #-------------------------------------------------
    #create the display (radar map type)
    #-------------------------------------------------
    display=pyart.graph.RadarMapDisplay(myradar)
    font={'size':10}
    matplotlib.rc('font',**font)
    fig=plt.figure(figsize=[15,8])

    #-------------------------------------------------
    #panel creation
    #-------------------------------------------------
    map_panel=[0.05,0.05,0.4,0.8]
    cut_panel=[0.55,0.1,0.4,0.7]
    colorbar_panel=[0.05,0.9,0.4,0.05]

    #-------------------------------------------------
    # map panel : field to plot and reflectivity contour
    #-------------------------------------------------
    ax1=fig.add_axes(map_panel)
    display.plot_ppi_map(
        field=field,sweep=sweep, vmin=vmin, vmax=vmax,
        lat_lines = lat_lines, lon_lines = lon_lines,
        max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
        title_flag=False,
        mask_outside = True,
        colorbar_flag=False,
        cmap = cmap,
        # basemap = ref_m,
        ax=ax1
        )

    #-------------------------------------------------
    #colorbar panel
    #-------------------------------------------------
    cbax=fig.add_axes(colorbar_panel)
    display.plot_colorbar(cax=cbax,orient="horizontal")

    #---------------------------------------
    #Save the plot in outloc directory or show it
    #---------------------------------------
    if option=='save':
        plt.savefig('{}Namoi_at_{}_el_{}_{}.png'.format(outloc,dts[0].strftime('%H%M_Z_on_%Y_%m_%d'),str(el1),reference),dpi=100)
    if option=='show':
        plt.show()
    

    
    
def makeMP4(field):
    #field may be equal to 'reflectivity', 'dop_velocity', 'spec_width' 
    #building input and output directory from the field information
    input_0=os.path.abspath("../plots/{}".format(field))
    output=os.path.abspath("../videos/{}".format(field))
    print(output)
    if not os.path.exists(output): os.makedirs(output)

    list=os.listdir(input_0)
    print(list)
    for angle in list:
        #move to the right repository
        os.chdir('{}/{}'.format(input_0,angle))
        print(os.getcwd())
        #create an apply the command to make the video
        cmd="ffmpeg -r 2 -pattern_type glob -i '*.png' -pix_fmt yuv420p {}/{}_{}.mp4".format(output,field,angle)
        print(cmd)
        os.system(cmd)
        print('Video created: {}/{}_{}.mp4'.format(output,field,angle))
        



