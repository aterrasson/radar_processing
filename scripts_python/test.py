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
# WIP nb 2
#-------------------------------------------------
myrad=pyart.aux_io.read_odim_h5(dirname+fls[30],file_field_names=True)
#plot_slice(myrad,point1=(149.63,-32),point2=(150.8,-32.2),field='DBZH')
# print('{},{}'.format(myrad.longitude,myrad.latitude) )
#plot_bolton_1_slices(myrad,point1=(150.39,-32),point2=(150.48,-32.4),field='DBZH',sweep=0,option='show')
#plot_bolton_2_slices(myradar=myrad,sweep=0,azimuth=[170,197],field="DBZH",option='show')


