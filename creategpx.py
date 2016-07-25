# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 11:27:31 2016

@author: Hxu
"""
import pandas as pd
import datetime as dt
#import matplotlib.pyplot as plt
df=pd.read_csv('http://nefsc.noaa.gov/drifter/drift_gomi_2015_3.csv',index_col=[0])  # read drifter csv file

names=df.index.unique().tolist() #get all  drifters' ID

f=open('drift123.gpx','w')

f.writelines("<?xml version='1.0' encoding='UTF-8'?>\n")
f.writelines("<gpx version='1.1' creator='Garmin Connect'\n")
f.writelines("  xsi:schemaLocation='http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd'\n")
f.writelines("  xmlns='http://www.topografix.com/GPX/1/1'\n")
f.writelines("  xmlns:gpxtpx='http://www.garmin.com/xmlschemas/TrackPointExtension/v1'\n")
f.writelines("  xmlns:gpxx='http://www.garmin.com/xmlschemas/GpxExtensions/v3' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>\n")
f.writelines("  <metadata>\n")
f.writelines("    <link href='connect.garmin.com'>\n")
f.writelines("      <text>Garmin Connect</text>\n")
f.writelines("    </link>\n")
f.writelines("    <time>2015-03-08T07:27:47.000Z</time>\n")
f.writelines("  </metadata>\n")
f.writelines("  <trk>\n")
f.writelines("    <name>Soller - Pollen</name>\n")
f.writelines("    <trkseg>\n")
name=names[1]
drifter=[]
df1=df.loc[name]
for x in range(len(df1)):
    
     #drifter.append([dt.datetime((2000+int(str(df1.index[0])[:2])),1,1,0,0)+dt.timedelta(df1.iloc[x][5]),df1.iloc[x][6],df1.iloc[x][7]])
    f.writelines('      <trkpt lon="'+str(df1.iloc[x][6])+'" lat="'+str(df1.iloc[x][7])+'">\n')
    f.writelines('        <ele>58.20000076293945</ele>\n')
    #f.writelines('        <time>2014-03-08T07:27:47.000Z</time>')
    f.writelines('        <time>'+(dt.datetime((2000+int(str(df1.index[0])[:2])),1,1,0,0)+dt.timedelta(df1.iloc[x][5])).strftime('%Y-%m-%dT%H:%M:%S')+'.000Z</time>\n')
    f.writelines('      </trkpt>\n')
f.writelines('    </trkseg>\n')
f.writelines('  </trk>\n')
f.writelines('</gpx>\n')
f.close()