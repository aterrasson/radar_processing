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

#for c,i in enumerate(fls):
#    print(i)
#print(c)
# outloc = '../plots/'     


#
#-------------------------------------------------
# creating a radar object from the specified file
# then plotting the velocity and reflectivity contourlines for each sweep and each available file
#-------------------------------------------------
# for c,i in enumerate(fls):
#     myrad=pyart.aux_io.read_odim_h5(
#         dirname + i,
#         file_field_names=True
#     )
#     for cs,sweep in enumerate(myrad.sweep_number['data']):

#         plot_bolton_bom(myradar=myrad,sweep=sweep,field='VRADH',option='save')
    
#     print('{} files processed over {}. {}% Done'.format(c+1,len(fls),(c+1)/len(fls)*100))



#-------------------------------------------------
# creating the video for each sweep
#-------------------------------------------------
#makeMP4('reflectivity')


#-------------------------------------------------
# plotting the top view and two azimuth slices
#-------------------------------------------------
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
# plot_bolton_2_slices(myradar=myrad,sweep=0,azimuth=[170,197],field="VRADH",option='show')

#-------------------------------------------------
# WIP
#-------------------------------------------------
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
# z,data,gap=give_my_point_a_value(point=(150.5,-32.3),myradar=myrad,field='VRADH',sweep=1)
# print(z,data,gap)
#create_line(start_point=(149.5,-31.8),end_point=(150.6,-32.4),nb_pt=15)

#-------------------------------------------------
# WIP nb 2
#-------------------------------------------------
myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
# LON=np.array(myrad.gate_longitude['data'])
# #print(LON)
# #print(LON.shape)
# LAT=np.array(myrad.gate_latitude['data'])
# #print(LAT)
# #print(LAT.shape)
# ALT=np.array(myrad.gate_altitude['data'])
# DATA=np.array(myrad.fields['VRADH']['data'])
# r_LON=np.linspace(150,151,100)
# r_LAT=np.linspace(-32.2,-32,2)
# r_ALT=np.linspace(0,10000,100)
# new_LON,new_LAT,new_ALT=np.meshgrid(r_LON,r_LAT,r_ALT)
# new_GRID=scipy.interpolate.griddata(
#     ( LON.flatten() , LAT.flatten(),ALT.flatten() ) ,
#     DATA.flatten(),
#     ( new_LON , new_LAT , new_ALT ),
#     method='linear'
# )

#-------------------------------------------------
# WIP nb 3
#-------------------------------------------------
plot_slice(myrad,point1=(150,-32.2),point2=(150.5,-32.2),field='VRADH')


