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
    """
    this function plots a field from aradar object, with contour reflectivity

    myradar - radar object from py art
    sweep - int, the sweep we will plot
    field - string 'DBZH' for reflectivity, 'VRADH' for doppler velocity, 'WRADH' for spec width
    contour field - string 'DBZH' for reflectivity, 'VRADH' for doppler velocity, 'WRADH' for spec width. untested with other value than 'DBZH'. field sed to plot the contour.
    option - string 'save' or 'show'
    """
    
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
    
    plot_point(lon=myradar.longitude['data'][0],lat=myradar.latitude['data'][0],ax=ax1)

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

def plot_point(point, angle, ax_to_plot,color,length,azimuth_to_trigo,lw=1):
     '''
     this function draws a line from a starting point to a specific angular direction
     
     ax_to_plot - axe object who will include the line
     point - Tuple (x, y)
     angle - Angle you want your end point at in degrees.
     length - Length of the line you want to plot (km in the basemap).
     azimuth_to_trigo - boolean, True if the angle argument is an azimuth, False otherwise

     '''

     # unpack the first point
     x, y = point

     # convert the trigonometric angle in an azimuth angle
     if azimuth_to_trigo==True:angle=-angle+90
     
     # find the end point
     length=length*1000
     endy = y+length * math.sin(math.radians(angle))
     endx = x+length * math.cos(math.radians(angle))

     # plot the points
     #ax_to_plot.set_ylim([0, 10])   # set the bounds to be 10, 10
     #ax.set_xlim([0, 10])
     ax_to_plot.plot([x, endx], [y, endy],'--',color=color,linewidth=lw)
     ax_to_plot.plot([endx],[endy],color=color,marker='o')

def plot_bolton_2_slices(myradar,sweep,azimuth,field,len_slice=180,option='show'):
    """
    this function allows to show a top view and two slice defined by chosen azimuth, starting at the radar position.

    the first figure is a ppi plot of the chosen field and two lines corresponding to the azimuth from the radar,
    the second figure rhi view of the first azimuth
    the third figure is a rhi view of the second azimuth

    myradar - radar object from which we want to plot data (tested for ppi mode only)
    sweep - int sweep to plot (corresponds to elevation if ppi mode)
    azimuth - 2-array [azimuth1, azimuth2]
    field - string, 'DBZH' for reflectivity,'VRADH' for dopple velocity,'WRADH' for spec width
    len_slice - int, length in km of the rhi construction
    option - string 'show' or 'save'
    """
    
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    #outloc = '../plots/' 
    tz=11
    el1 = myradar.get_elevation(sweep)[0]
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])


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
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/spec_width/angle_{}/'.format(el1),0,15,'Spec Width (m/s)',pyart.graph.cm.BuDOr12,'Spec_width']

    #-------------------------------------------------
    #creating a second radar with rhi data from the ppi data
    #-------------------------------------------------
    if azimuth is int:azimuth=[azimuth]
    max_alt_rhi=12
    myrad_rhi=pyart.util.cross_section_ppi(myradar,azimuth)
    for n,a in enumerate(azimuth):
        print('azimuth = {} \n'.format(a))
        for ele in myrad_rhi.get_elevation(n):
            print(ele)
    #-------------------------------------------------
    #create the displays (radar map type)
    #-------------------------------------------------
    display=pyart.graph.RadarMapDisplay(myradar)
    display_rhi=pyart.graph.RadarDisplay(myrad_rhi)
    font={'size':10}
    matplotlib.rc('font',**font)
    fig=plt.figure(figsize=[15,8])

    #-------------------------------------------------
    #panel creation
    #-------------------------------------------------
    map_panel=[0.05,0.05,0.4,0.8]
    slice_panel_1=[0.55,0.1,0.4,0.3]
    slice_panel_2=[0.55,0.5,0.4,0.3]
    colorbar_panel=[0.05,0.9,0.4,0.05]

    #-------------------------------------------------
    # map panel : field to plot and reflectivity contour, lines of azimuth
    #-------------------------------------------------
    ax=fig.add_axes(map_panel)
    
    display.plot_ppi_map(
        field=field,sweep=sweep, vmin=vmin, vmax=vmax,
        lat_lines = lat_lines, lon_lines = lon_lines,
        max_lat = max_lat, min_lat = min_lat, min_lon = min_lon, max_lon = max_lon,
        title_flag=False,
        mask_outside = True,
        colorbar_flag=False,
        cmap = cmap,
        # basemap = ref_m,
        ax=ax
        )
    
    # getting the radar position in basemap coordinates and plotting it as a point
    lon,lat=myradar.longitude['data'][0],myradar.latitude['data'][0]
    x,y=display.basemap(lon,lat)
    
    # plotting the two lines corresponding to the two azimuths
    plot_point( point=(x,y ), angle=azimuth[0], length=len_slice, ax_to_plot=ax,color='red',azimuth_to_trigo=True,lw=2)
    plot_point( point=(x,y ), angle=azimuth[1], length=len_slice, ax_to_plot=ax,color='blue',azimuth_to_trigo=True,lw=2)
    ax.plot([x],[y],marker='o',color='red')

    #write the time as text on the figure
    ax.text(x=0.1,y=0.9,s='t={}'.format(dts[0].strftime('%H%M')),fontsize=20,transform=ax.transAxes )


    #-------------------------------------------------
    #slice panel_1: plot a slice corresponding to the first azimuth
    #-------------------------------------------------
    ax1=fig.add_axes(slice_panel_1)
    ax1.set_ylim([0,max_alt_rhi])
    ax1.set_xlim([0,len_slice])
    display_rhi.plot(
        field=field,
        sweep=0,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        colorbar_flag=False,
        title_flag=False,
        ax=ax1
    )
    ax1.grid(True)

    # coloriziing the axis the same color a the line as on the ppi map
    ax1.xaxis.set_tick_params(color='red',labelcolor='red',labelsize=15)
    #plotting min and max elevation
    plot_point(point=(0,0),angle=myrad_rhi.get_elevation(sweep=0)[0],length=5,ax_to_plot=ax1,color='black',azimuth_to_trigo=False)
    plot_point(point=(0,0),angle=myrad_rhi.get_elevation(sweep=0)[-1],length=5,ax_to_plot=ax1,color='black',azimuth_to_trigo=False)

    #write the azimuth as text on the figure
    ax1.text(x=0.1,y=0.9,s='azimuth = {} deg'.format(azimuth[0]),fontsize=20,transform=ax1.transAxes )

    #-------------------------------------------------
    #slice panel_2: plot the slice of the second azimuth
    #-------------------------------------------------
    ax2=fig.add_axes(slice_panel_2)
    ax2.set_ylim([0,max_alt_rhi])
    ax2.set_xlim([0,len_slice])
    display_rhi.plot(
        field=field,
        sweep=1,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        colorbar_flag=False,
        title_flag=False,
        ax=ax2
    )
    ax2.grid(True)

    # coloriziing the axis the same color a the line as on the ppi map
    ax2.xaxis.set_tick_params(color='blue',labelcolor='blue',labelsize=15)
    
    #plotting min and max elevation
    plot_point(point=(0,0),angle=myrad_rhi.get_elevation(sweep=1)[0],length=5,ax_to_plot=ax2,color='black',azimuth_to_trigo=False)
    plot_point(point=(0,0),angle=myrad_rhi.get_elevation(sweep=1)[-1],length=5,ax_to_plot=ax2,color='black',azimuth_to_trigo=False)

    #write the azimuth as text on the figure
    ax2.text(x=0.1,y=0.9,s='azimuth = {} deg'.format(azimuth[1]),fontsize=20,transform=ax2.transAxes )

    #-------------------------------------------------
    #colorbar panel
    #-------------------------------------------------
    cbax=fig.add_axes(colorbar_panel)
    display_rhi.plot_colorbar(label=colorbar_label,cax=cbax,orient="horizontal")

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
        



