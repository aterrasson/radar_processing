#
# coding: utf-8
#
# In[3]:
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
#print(fls)
#for c,i in enumerate(fls):
#    print(i)
#print(c)    


#
#-------------------------------------------------
# creating a radar object from the specified file
# then plotting on field and reflectivity contourlines for each sweep and each available file
#-------------------------------------------------
# for c,i in enumerate(fls):
#     myrad=pyart.aux_io.read_odim_h5(
#         dirname + i,
#         file_field_names=True
#     )
#     print('file {} is being processed'.format(i))
#     #pytda.calc_turb_vol(radar=myrad,verbose=False,name_dz='DBZH',name_sw='WRADH')
#     for cs,sweep in enumerate(myrad.sweep_number['data']):

#         plot_bolton_bom(myradar=myrad,sweep=sweep,field='DBZH',option='save')
    
#     print('{} files processed over {}. {}% Done'.format(c+1,len(fls),(c+1)/len(fls)*100))



#-------------------------------------------------
# creating the video for each sweep on the name field
#-------------------------------------------------
#makeMP4('turbulence')


#-------------------------------------------------
# plotting the top view and two azimuth slices
#-------------------------------------------------
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
# plot_bolton_2_slices(myradar=myrad,sweep=0,azimuth=[170,197],field="VRADH",option='show')


#-------------------------------------------------
# Plotting the top view and one arbitrary slice defined by two points
#-------------------------------------------------
#myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
#plot_slice(myrad,point1=(149.63,-32),point2=(150.8,-32.2),field='DBZH')
#plot_bolton_1_slices(myrad,point1=(150.39,-32),point2=(150.48,-32.4),field='DBZH',sweep=0,option='show')


#-------------------------------------------------
# Plotting one field, possibly the turbulence if the the second line is uncommented
#-------------------------------------------------
#myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
#pytda.calc_turb_vol(radar=myrad,verbose=True,name_dz='DBZH',name_sw='WRADH')
#plot_bolton_bom(myradar=myrad,sweep=0, field='WRADH', option='show')

#-------------------------------------------------
# Plot of the time evolution of 1 variable
#-------------------------------------------------
#total_ref(my_sweeps=[0,1,2,3,4,5,6], window=(146.9,-32.6,151.2,-31.8),time_steps=(1100,2000),dirname='../NamoiData/',st_dev=False,option='show')

#-------------------------------------------------
# WIP basemap
#-------------------------------------------------
myrad=pyart.aux_io.read_odim_h5(dirname+fls[32],file_field_names=True)
plot_bolton_bom_V2(myradar=myrad,sweep=0, field='DBZH', option='save')
# map=Basemap(llcrnrlon=min_lon-3,
#             llcrnrlat=min_lat-3,
#             urcrnrlon=max_lon+3,
#             urcrnrlat=max_lat+3,
#             projection='tmerc',
#             resolution='i',
#             #lon_0=(min_lon+max_lon)/2,
#             #lat_0=(min_lat+max_lat)/2,
#             epsg=3112
#             )

# map.drawcoastlines()
# map.imshow(plt.imread('../basemap/coldfront/no_bm.png'))
#map.fillcontinents(color='coral',lake_color='aqua')
#plt.show()
#plt.savefig('../basemap/coldfront/')
#height(5.6,120)
#height(2.4,150)


print("\nIt's my liiiiife\n")

