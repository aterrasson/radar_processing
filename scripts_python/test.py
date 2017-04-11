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
#     for cs,sweep in enumerate(myrad.sweep_number['data']):

#         plot_bolton_bom(myradar=myrad,sweep=sweep,field='DBZH',option='save')
    
#     print('{} files processed over {}. {}% Done'.format(c+1,len(fls),(c+1)/len(fls)*100))

#-------------------------------------------------
# myrad=pyart.aux_io.read_odim_h5(dirname+fls[20],file_field_names=True)
# plot_bolton_bom(myradar=myrad,sweep=0,field='WRADH',option='show')
#print('nb of sweep: {}'.format(myrad.nsweeps))

#for s in myrad.sweep_number['data']:
#     el=myrad.get_elevation(s)[0]
#     print('sweep={}, el={}'.format(s,el) )
#-------------------------------------------------
#for f in myrad.fields.keys():
#    print(f)
makeMP4('reflectivity')

