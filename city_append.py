#To use this city append script, you need to have python and pandas installed.

#This script will take an export from Revere Mobile, match it on zipcode to a file
#containing state information, and produce a file of just Mobile # and city with their
#Revere Mobile metadata IDs as the column headers

#To run it:
#1. Download http://download.geonames.org/export/zip/US.zip and save US.txt in this directory
#2. Also save the export from Mobile in this directory. Supposed it's called export.csv
#3. At the command line prompt, type:
#   python city_append.py export.csv

import sys
import pandas as pd

#Get the name of the export file from the command line
filename = sys.argv[-1]

#Read just the Mobile # and zipcode into df_export
fields = ['Mobile #','zipcode']
df_export = pd.read_csv(filename, skipinitialspace=True, usecols=fields)
df_export['zipcode'] = df_export['zipcode'].astype(str).str.zfill(5)

#Read US.txt into df_zip_info, add header row, then delete all but zipcode and city
df_zip_info = pd.read_csv('US.txt', sep='\t',header=None)
df_zip_info.columns = ['Country', 'zipcode','city','state_full_name','state',
'admin_name2','admin code2','admin name3','admin code3','latitude','longitude','accuracy']
df_zip_info = df_zip_info[['zipcode','city']]
df_zip_info['zipcode'] = df_zip_info['zipcode'].astype(str).str.zfill(5)

#Left-join df_export and df_zip_info on zipcode, store in df_merged
df_merged = df_export.merge(df_zip_info, on='zipcode', how='left')

#Keep only Mobile # and city, delete rows with no city
df_merged = df_merged[['Mobile #','city']]
df_merged = df_merged[df_merged.city.notnull()]

#Rename columns with Revere Mobile metadata IDs
#If uploading to SEIU, use
#df_merged.columns = ['msisdn','4f83b5a349f0237df0577898'] #SEIU platform
df_merged.columns = ['msisdn','4f83b5a349f0237df0577895'] #Main platform

#Send dv_merged to a csv, eliminating the index
df_merged.to_csv(filename[0:-4]+'_city_append.csv',sep=',',index=False)
