#
# coding: utf-8
#
# In[3]:
#
#
#imports
from imports import *

    #---------------------------------------
    # Range of lat/lonfor the plot
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
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/reflectivity/angle_{}/'.format(el1),0,50,'Reflectivity (dBZ)',pyart.graph.cm.LangRainbow12,'Reflectivity']
        
    #plot spec width
    elif field=='WRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/spec_width/angle_{}/'.format(el1),0,15,'Spec Width (m/s)',pyart.graph.cm.BuDOr12,'Spec_width']

    #-------------------------------------------------
    #creating a second radar with rhi data from the ppi data
    #-------------------------------------------------
    if azimuth is int:azimuth=[azimuth]
    max_alt_rhi=12
    myrad_rhi=pyart.util.cross_section_ppi(myradar,azimuth)

    # print the available elevation for the chosen azimuth
    # for n,a in enumerate(azimuth):
    #     print('azimuth = {} \n'.format(a))
    #     for ele in myrad_rhi.get_elevation(n):
    #         print(ele)
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

def give_my_point_a_value(point,myradar,field,sweep):
    
    """
    return altitude and field value from the closest radar point available 
    point - 2-tuple: (lon,lat) in WG84
    myradar - radar object (only tested with ppi radar)
    sweep - int

    return:
    z - double (m) altitude of the closest measured point
    data - double (unit depends on the chosen field)
    gap - double sum of the latitude gap and the lontitude gap between the input point and the closest radar point
    """
    x,y=point
    # selecting the data from the right sweep
    start=myradar.get_start(sweep)
    end=myradar.get_end(sweep)+1
    
    # We find the minimum distance between our point and the radar data
    # A is the list of longitude gaps added to latitude gaps
    A=[
        abs(x-xrad)+abs(y-yrad)
        for xrad,yrad in zip (myradar.gate_longitude['data'][start:end], myradar.gate_latitude['data'][start:end])
    ]
    
    # conversion into an array
    B=np.array(A)
    
    # get the matrix coordinates of closest radar point
    minx,miny=np.unravel_index( np.argmin(B) , B.shape )

    #saving the gap value
    gap=B[minx,miny]
    #print(gap)

    #affecting z and field value of the closest radar point
    z,data=myradar.gate_altitude['data'][start:end][minx][miny],myradar.fields[field]['data'][start:end][minx][miny]
    print('closest point from ({} E,{} N) found is ({} E,{} N)'.format(x,y,myradar.gate_longitude['data'][start:end][minx][miny],myradar.gate_latitude['data'][start:end][minx][miny]) )

    return z,data,gap


def plot_slice(myradar,point1,point2,field):
    """
    The goal is to plot a slice of a field along a chosen line

    Steps:
    1 - extract the gates for longitude/latitude/altitude/chosen field
    2 - narrow the values to fit a chosen window (the line has to be included in the window) to accelerate the regridding operation
    3 - generate a meshgrid and rotate it so one of the axis becomes the chosen line. Then interpolate our field on the meshgrid
    4 - extract the plan formed by the chosen line and the z axis
, mask the nans values    
    5 - plot the plan with the value and the field

    Inputs:
    radar - radar object from pyart
    point1 - tuple (longitude ,latitude) first point of the line
    point2 - tuple (longitude ,latitude) last point of the line
    field - string 'VRADH' or 'WRADH' or 'DBZH' field to plot

    Possibles ways of improvements:
    - 
    - Reducing the windows size by having a window parallel to the line (currently the window is parallel to the longitude axe)
    - Modify the size of the meshgrid we interpole on to better match the number of gates along the chosen line

    """
    #-------------------------------------------------------
    # Step 1
    #-------------------------------------------------------

    # get the gates
    flat_LON=np.array(myradar.gate_longitude['data']).flatten()
    flat_LAT=np.array(myradar.gate_latitude['data']).flatten()
    flat_ALT=np.array(myradar.gate_altitude['data']).flatten()
    flat_DATA=np.array(myradar.fields[field]['data']).flatten()

    #-------------------------------------------------------
    # Step 2
    #-------------------------------------------------------
    
    # getting the start/end points
    lon1,lat1=point1
    lon2,lat2=point2
    
    # sizing the window
    min_lon=min(lon1,lon2)-0.01
    min_lat=min(lat1,lat2)-0.01
    max_lon=max(lon1,lon2)+0.01
    max_lat=max(lat1,lat2)+0.01

    # reducing the data to the window
    index_lon=[]
    index_lat=[]
    [index_lon.append(index ) for index,p in enumerate(flat_LON) if p<max_lon and p>min_lon]
    [index_lat.append(index ) for index,p in enumerate(flat_LAT) if p<max_lat and p>min_lat]
    index_window=list(set(index_lon) & set(index_lat))
    #print('len index_lon = {}'.format(len(index_lon)))
    #print('len index_lat = {}'.format(len(index_lat)))
    
    # Feedback on the window dimension and size
    print("""
Window dimensions:

    ({0:.5},{3:.5})-------------------------({2:.5},{3:.5})
          |                                          |
          |                                          |
          |                                          |
    ({0:.5},{1:.5})-------------------------({2:.5},{1:.5})


    """.format(min_lon,min_lat,max_lon,max_lat)
)
    print('Number of points in the window = {}'.format(len(index_window)))

    flat_LON=flat_LON[index_window]
    flat_LAT=flat_LAT[index_window]
    flat_ALT=flat_ALT[index_window]
    flat_DATA=flat_DATA[index_window]

    #print('{}\n\n{}'.format(flat_LON,flat_LAT))

    #-------------------------------------------------------
    # Step 3
    #-------------------------------------------------------

    # create a meshgrid starting at point1 and parallelto the logitude axis. the lenght of the meshgrid is the one of the line

    # getting the lenght of the chosen line and the angle from the longitude axis
    L=np.sqrt((lon2-lon1)**2+(lat2-lat1)**2)
    delta=-math.atan((lat2-lat1)/(lon2-lon1))
    print('Lenght= {0:.5}deg , Angle = {1:.5}rad'.format(L,delta))
    print("""
    ---------------------------------------------------
                Creating the new meshgrid
    ---------------------------------------------------
""")
    # creating the axis of the meshgrid 
    x1=np.linspace(lon1,lon1+L,100)
    y1=np.linspace(lat1-0.01,lat1+0.01,3)
    z1=np.linspace(0,10000,30)
    
    # creating the meshgrid
    X1,Y1,Z1=np.meshgrid(x1,y1,z1)

    # rotate the meshgrid
    c,s=np.cos(delta),np.sin(delta)
    
    X2=c*(X1-lon1)+s*(Y1-lat1)
    Y2=-s*(X1-lon1)+c*(Y1-lat1)
    Z2=Z1
    X2=X2+lon1
    Y2=Y2+lat1
    print('Meshgrid created. Number of points = {}'.format(len(X2.flatten())))
    print("""
    ---------------------------------------------------
                  Starting the interpolation
    ---------------------------------------------------
""")
    #interpolation on the new meshgrid
    new_DATA=scipy.interpolate.griddata(
        ( flat_LON , flat_LAT , flat_ALT ),
        flat_DATA,
        ( X2 , Y2 , Z2 ),
        #method='linear'
        method='nearest'
    )
    # [print(a) for a in zip(X2.flatten(),Y2.flatten(),Z2.flatten(),new_DATA.flatten() ) ]
        
    #-------------------------------------------------------
    # Step 4
    #-------------------------------------------------------
    
    # extracting the slice corresponding to the chosen line
    X,Z,D=X2[1,:,:],Z2[1,:,:],new_DATA[1,:,:]
    
    # masking the nans in the data
    Dm=np.ma.masked_where(np.isnan(D),D)
    # print(Dm)

    #-------------------------------------------------------
    # Step 5
    #-------------------------------------------------------
    print("""
    ---------------------------------------------------
                     Interpolation done
    ---------------------------------------------------
""")
    return(X-lon1,Z,Dm)

    
def plot_bolton_1_slices(myradar,point1,point2,field,sweep=0,option='show'):
    """
    
    This function allows to show a top view and one slic defined by two point.

    Inputs:

    myradar - radar object from which we want to plot data (tested for ppi mode only)
    sweep - int sweep to plot the ppi part (corresponds to elevation if ppi mode)
    point1, point2 - Tuple (lon,lat). Start ans end of the slice
    field - string, 'DBZH' for reflectivity,'VRADH' for dopple velocity,'WRADH' for spec width
    option - string 'show' or 'save'

    Outputs:

    Either a displayed plot or a saved plot depending on the value of option

    """
    
    vol_t = num2date(myradar.time['data'], myradar.time['units'])[0]
    #outloc = '../plots/' 
    tz=11
    el1 = myradar.get_elevation(sweep)[0]
    dts = num2date(myradar.time['data'] + tz*60.*60., myradar.time['units'])


    #-------------------------------------------------
    # specifying the field parameters
    #-------------------------------------------------
    #plot of velocity
    if field=='VRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/dop_velocity/angle_{}/'.format(el1),-15,15,'Doppler Velocity (m/s)',pyart.graph.cm.BuDOr12,'dop_Velocity']
        
    #plot of reflectivity
    elif field=='DBZH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/reflectivity/angle_{}/'.format(el1),0,50,'Reflectivity (dBZ)',pyart.graph.cm.LangRainbow12,'Reflectivity']
        
    #plot spec width
    elif field=='WRADH':
        [outloc,vmin,vmax,colorbar_label,cmap,reference]=['../plots/spec_width/angle_{}/'.format(el1),0,15,'Spec Width (m/s)',pyart.graph.cm.BuDOr12,'Spec_width']

   #-------------------------------------------------
    #create the displays (radar map type)
    #-------------------------------------------------
    display=pyart.graph.RadarMapDisplay(myradar)
    font={'size':10}
    matplotlib.rc('font',**font)
    fig=plt.figure(figsize=[8,15])

    #-------------------------------------------------
    #panel creation
    #-------------------------------------------------
    map_panel=[0.05,0.55,0.8,0.4]
    slice_panel_1=[0.05,0.05,0.8,0.4]
    colorbar_panel=[0.05,0.47,0.9,0.02]

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
    
    # plotting the line of the cross section
    x1,y1=display.basemap(point1[0],point1[1])
    x2,y2=display.basemap(point2[0],point2[1])
    ax.plot([x1,x2],[y1,y2],'k--',lw=2)

    #write the time as text on the figure
    ax.text(x=0.1,y=0.8,s='t={}\nsweep = {}'.format(dts[0].strftime('%H%M'),sweep),fontsize=15,transform=ax.transAxes )

    # write the coordinates of the two points
    ax.text(
        x=0.5,y=0.8,s='({}{})\n ({}{})'.format(point1[0],point1[1],point2[0],point2[1]),
        fontsize=15, transform=ax.transAxes
    )


    #-------------------------------------------------
    #slice panel_1: plot a slice corresponding to the chosen line
    #-------------------------------------------------
    X,Z,D=plot_slice(myradar=myradar,field=field,point1=point1,point2=point2)

    
    ax1=fig.add_axes(slice_panel_1)
    ax1.pcolormesh(
        X,Z,D,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        #colorbar_flag=False,
        #title_flag=False,
    )
    ax1.grid(True)



    #-------------------------------------------------
    #colorbar panel
    #-------------------------------------------------
    cbax=fig.add_axes(colorbar_panel)
    display.plot_colorbar(label=colorbar_label,cax=cbax,orient="horizontal")

    #---------------------------------------
    #Save the plot in outloc directory or show it
    #---------------------------------------
    if option=='save':
        plt.savefig('{}Namoi_at_{}_el_{}_{}.png'.format(outloc,dts[0].strftime('%H%M_Z_on_%Y_%m_%d'),str(el1),reference),dpi=100)
    if option=='show':
        plt.show()
    

    
    
    

