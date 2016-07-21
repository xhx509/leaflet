# -*- coding: utf-8 -*-
"""
Routine to extract temperature data as telemetered by AP2s
originally coded by JiM in Feb 2015 similar to "getfix.py" for drifters
modified by Huanxin 
note: The input datafile, in fact, is the same for drifters
"""
import sys
#hardcode path of modules
#sys.path.append("/home3/ocn/jmanning/py/") #3
#hardcode path of input (1) and output data (2) 
#path1="/net/data5/jmanning/drift/" # input data directory
#path2="/net/drifter/"    # output directory
#inputfile="raw2013.dat"
sys.path.append("/home3/ocn/jmanning/py/") #3
#hardcode path of input (1) and output data (2) 
path1="/net/data5/jmanning/drift/" # input data directory
#path2="/net/nwebserver/drifter/"    # output directory
path2='C:/pycodes/'
inputfile="raw2013.dat"

from matplotlib.dates import date2num
import time
from getap2s_functions import gettemps,read_codes,trans_latlon # this module is a modification of the getfix_functions
#from conversions import distance
import subprocess
import datetime
import numpy as np 
import folium
#docks at woods hole, PJ, CapeMay... where data is test only still need to add Gloucester, Newburyport, Hampton. etc
dock_lats=[41.5701,41.3166,38.95694]
dock_lons=[-70.6200,-70.5,-74.87449]

# get "including" (list of ESNs), "startyd", and "endyd" for this case using getap2s_function 
print sys.argv[1] # where input argument is the name of the case like, for example, 'getemolt_2015'
[including,caseid,startyd,endyd]=gettemps(sys.argv[1])
print 'ESNs = '+str(len(including))
#example: 
#including=[320241, 322134, 328420, 368537, 327192, 368742] is the list of ESNs
#caseid=[1, 1, 1, 1, 1, 1] # consecutive use of these transmitter
# get "ide" and "depth" for specific ESNs from /data5/jmanning/drift/codes_temp.dat
#where "ide" is the eMOLT site
[esn,ide,depth]=read_codes('codes.dat')

# update the raw datafile by running perl routine getfix.plx
if sys.argv[1]=='drift_2013.dat': # we assume the drifter process is running this case
  pipe = subprocess.Popen(["perl", "/home/jmanning/drift/getfix.plx"])

#f_output=open(path2+str(sys.argv[1]),'w')

map_1 = folium.Map(location=[41.572, -70.6072],
                   zoom_start=12,
                   tiles='http://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
                   attr= 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC',
	)

colors=['red', 'darkred', 'orange', 'green', 'darkgreen', 'blue', 'purple', 'darkpuple', 'cadetblue']
dictionary = dict(zip(esn, colors))

for i in range(1,len(including)): # note: I am skipping vessel_1 since that was just at the dock test
  #print startyd[i],endyd[i]
  #open the raw input datafile 
  f = open(inputfile,'r') 
  #     f_output.write("ID        ESN   MTH DAY HR_GMT MIN  YEARDAY    LON           LAT     DEPTH TEMP\n")
  #start parsing the variables needed from the raw datafile
  for line in f:
      if line[1:4]=='esn' and line[11]=='<': #AP2s!!:
          idn1=int(line[7:11]) # picks up ESN
          #print idn1
          if idn1==including[i]:
                index_idn1=np.where(str(idn1)==np.array(esn))[0] # Is this ESN in the codes_temp?
                # some idn1 can not fine in ESN (codes_temps.dat), so I can not find it's id and depth
                if index_idn1.shape[0]<>0: # if this unit is included in the codes_temp.dat file
                    #print index_idn1,ide
                    #id_idn1=int(ide[index_idn1[caseid[i]-1]]) # where "caseid" is the consecutive time this unit was used
                    id_idn1=ide[index_idn1[caseid[i]-1]] # where "caseid" is the consecutive time this unit was used
                    depth_idn1=-1.0*float(depth[index_idn1[caseid[i]-1]]) # make depth negative
                    skip1=next(f) #skip one line
                    if skip1[1:9]=="unixTime":
                        unixtime=int(skip1[10:20]) #get unix time
                        #convert unixtime to datetime
                        time_tuple=time.gmtime(unixtime)
                        yr1=time_tuple.tm_year
                        mth1=time_tuple.tm_mon
                        day1=time_tuple.tm_mday
                        hr1=time_tuple.tm_hour
                        mn1=time_tuple.tm_min
                        yd1=date2num(datetime.datetime(yr1,mth1,day1,hr1,mn1))-date2num(datetime.datetime(yr1,1,1,0,0))
                        datet=datetime.datetime(yr1,mth1,day1,hr1,mn1,tzinfo=None)                               
                        skip2=next(f) # skip one line
                        #skip3=next(f)
                        skip4=next(f)
                        #if i==5:
                        #  print datet
                        if datet>startyd[i] and datet<endyd[i] and skip4[17]<>9 and skip4[17:19]<>27:
                          data_raw=skip4[48:]
                          try:
                            if (int(data_raw[27:31])<900) or (int(data_raw[27:31])>1100):
                              #print data_raw
                              lat,lon=trans_latlon(data_raw)    # transfer lat,lon from Hex to Decimal
                                #check to see if this is a dock side test
                              dist_bear=[]
                              for kk in range(len(dock_lats)):
                                  #dist_bear.append(distance((lat,lon),(dock_lats[kk],dock_lons[kk])))
                              #if min([x[0] for x in dist_bear])>3.0: # if greater than one kilometers from all docks  
                                  if (lat<89.) and (data_raw[21]!='B') and (data_raw[27]!='D') and (data_raw[31]!='D') and (data_raw[21]!='D') and (data_raw[32]!='D') and (datet>datetime.datetime(2016,6,1,1,1)) and (data_raw[20]!='B'): # otherwise no good GPS
                                    #print    float(data_raw[21:26])        
                                    meandepth=float(data_raw[21:24])              
                                    rangedepth=float(data_raw[24:27])              
                                    len_day=float(data_raw[27:30])/1000.            
                                    mean_temp=float(data_raw[30:34])/100
                                    try:
                                      float(data_raw[34:38]) # this problem arose in March 2016
                                      sdevia_temp=float(data_raw[34:38])/100           #standard deviation temperature
                                    except ValueError:
                                      sdevia_temp=0.0  
                                    if mean_temp<30.0: #eliminates obviously bad data
                                      lastime= str(mth1).rjust(2)+ " " + str(day1).rjust(2)+" " +str(hr1).rjust(3)+ " " +str(mn1).rjust(3)
                                      #f_output.write(str(id_idn1).rjust(10)+" "+str(idn1).rjust(7)+ " "+str(mth1).rjust(2)+ " " +
                                       #   str(day1).rjust(2)+" " +str(hr1).rjust(3)+ " " +str(mn1).rjust(3)+ " " )
                                      #f_output.write(("%10.7f") %(yd1))
                                      #f_output.write(" "+str(lon).rjust(10)+' '+str(lat).rjust(10)+ " " +str(float(depth_idn1)).rjust(4)+ " "
                                      #        +str(np.nan))
                                      #f_output.write(" "+("%10.5f") %(lon)+' '+("%10.5f") %(lat)+' '+str(float(depth_idn1)).rjust(4)+ " "
                                         # +str(np.nan))
                                      #f_output.write(" "+str(meandepth).rjust(10)+' '+str(rangedepth).rjust(10)+' '+str(len_day).rjust(10)+  " " +str(mean_temp).rjust(4)+ " "
                                      #        +str(sdevia_temp)+'\n')            
                                      #f_output.write(" "+str(meandepth).rjust(10)+' '+str(rangedepth).rjust(10)+' '+str(len_day).rjust(10)+  " " +("%6.2f") %(mean_temp)+ " "
                                       #   +("%6.2f") %(sdevia_temp)+("%6.0f") %(yr1)+'\n')   
                                      
                                      
                                      html='''
                                            <h1> This is CTD DATA</h1><br>
                                            This is vessel:  
                                            <p>
                                            
                                            <code>
                                            '''+datet.strftime('%d-%b-%Y  %H:%M:')+ '<br>meandepth(m): '+str(meandepth).rjust(10)+'<br>rangedepth(m): '+str(rangedepth).rjust(10)+'<br>time_period(minutes): '+str(len_day*60*24).rjust(10) +'<br>meantemp(C): ' +str(mean_temp).rjust(4)+'<br>sdevia_temp(C): '+str(sdevia_temp)+''''
                                            </code>
                                            </p>
                                            '''
                                      iframe = folium.element.IFrame(html=html, width=500, height=300)
                                      popup = folium.Popup(iframe, max_width=1400)
                                      folium.Marker([lat,lon], popup=popup,icon=folium.Icon(color=dictionary[str(idn1)])).add_to(map_1)
                                      '''
                                      folium.Marker([lat, lon], popup=( datet.strftime('%d-%b-%Y  %H:%M:')+
                                      "      meandepth: "+str(meandepth).rjust(10)+"<br>"+"rangedepth: "
                                      +str(rangedepth).rjust(10)+"\n"+"time_period: "+str(len_day).rjust(10) +"\n"+"meantemp: " 
                                      +str(mean_temp).rjust(4)+
                                      "\nsdevia_temp: "+str(sdevia_temp)),icon=folium.Icon(color=dictionary[str(idn1)])).add_to(map_1) 
                                      '''
                                  else:
                                    print 'Bad GPS '+str(lat)+'N,'+str(lon)+'W for unit '+str(id_idn1).rjust(10)+' '+str(idn1).rjust(7)+' on '+str(mth1).rjust(2)+"/"+str(day1).rjust(2)+" " +str(hr1).rjust(3)            
                          except:
                             print ''         
  f.close()
#f_output.close()
map_1.save('map.html')  
#noext=sys.argv[1]
#pipe4 = subprocess.Popen(['/anaconda/bin/python','/home/jmanning/drift/ap2s2xml.py',noext[:-4]])  
