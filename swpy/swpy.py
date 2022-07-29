import sys 
import os
import numpy as np
from numpy import loadtxt
import pandas as pd

#test input
sys.argv = ([

    'nil','/flat2/3dnvgdaz21/python_ab/swath_table_creator/dmgseq_ns21k_updated.csv',
    '15000','25000','499','-1','3','DM_SEQ','SMIN_DUMP_B4GWE','SMAX_DUMP_B4GWE','2',
    'VESSEL_NO','CHUNK','NOTES'
     
    ])

#location of csv containing all saillines
table_csv_loc = sys.argv[1]
table_csv_loc_out = table_csv_loc.split('.')[0] + '_sw.csv'

#min and max seishot of survey for splitting lines
min_seishot = int(sys.argv[2])
max_seishot = int(sys.argv[3])

#swath dimensions
sw_length = int(sys.argv[4])
sw_overlap = int(sys.argv[5])
sw_time = int(sys.argv[6])

#calculate no of swaths
no_of_sw = (max_seishot - min_seishot)//(sw_length-sw_overlap)
tot_time = no_of_sw * sw_time

#swath dimensions
profile_col = sys.argv[7]
seismin_col = sys.argv[8]
seismax_col = sys.argv[9]
no_of_guns = int(sys.argv[10])

#number of extra columns to include in the sw table 
n_columns = len(sys.argv)-11
columns_in = [0]*n_columns

#assign all column names to array
for i in range(n_columns):
    columns_in[i] = sys.argv[i+11]
columns_all = [profile_col,seismin_col,seismax_col] + columns_in

#read in sailline table from csv
m_prof = pd.read_csv(table_csv_loc)
no_of_lines = len(m_prof)

#keep only selected columns
m_prof_ref = pd.DataFrame(data=m_prof,
          index=np.array(range(no_of_lines)),
          columns = columns_all)

#repeat each row (no_of_sw) times
m_prof_rep = pd.DataFrame(np.repeat(m_prof_ref.values,no_of_guns*no_of_sw,axis=0), columns = columns_all)


#initialise variables that need to be calculated
table_len = len(m_prof_rep)
gun = np.zeros(table_len)
sw_min = np.zeros(table_len)
sw_max = np.zeros(table_len)
sw = np.zeros(table_len)

#assign correct sw,gun value as well as limits for each row
for i in range(no_of_lines):
    for j in range(no_of_guns):        
        for k in range(no_of_sw):
            sw[i*no_of_guns*no_of_sw + j*no_of_sw + k] = str(k+1).zfill(2)
            gun[i*no_of_guns*no_of_sw + j*no_of_sw + k] = j+1
            sw_min[i*no_of_guns*no_of_sw + j*no_of_sw + k] = min_seishot + k * (sw_length-sw_overlap)
            sw_max[i*no_of_guns*no_of_sw + j*no_of_sw + k] = sw_min[i*no_of_guns*no_of_sw + j*no_of_sw + k] + sw_length
              
m_prof_rep["GUN"] = gun.astype(int)
m_prof_rep["SW"] = sw.astype(int)
m_prof_rep["SW"] = m_prof_rep["SW"].astype(str).str.zfill(2)
m_prof_rep["SW_MIN"] = sw_min.astype(int)
m_prof_rep["SW_MAX"] = sw_max.astype(int)     
        
m_prof_rep['KEEP'] = np.where((m_prof_rep['SW_MIN'] < m_prof_rep[seismax_col]) & (m_prof_rep['SW_MAX'] > m_prof_rep[seismin_col])
                     , 1, 0)
   
m_prof_keep = m_prof_rep[m_prof_rep['KEEP'] == 1]      
m_prof_keep['SW'] = m_prof_keep['SW'].astype(str)
m_prof_keep['PROFILE'] = m_prof_keep[profile_col].astype(str) + '_' +  m_prof_keep['GUN'].astype(str) + '_' + m_prof_keep['SW']



columns_all = ['PROFILE'] + [profile_col,seismin_col,seismax_col] + columns_in + ['SW_MIN','SW_MAX']


#keep only selected columns
m_prof_fin = m_prof_keep[columns_all]

m_prof_fin.to_csv(table_csv_loc_out,index=False)
