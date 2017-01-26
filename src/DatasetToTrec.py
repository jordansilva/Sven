
# coding: utf-8

# In[24]:

import os
from datetime import datetime
import pandas as pd
import numpy as np


# In[19]:

# #### LOADING TRAINING DATA
def load_data(file):
    print('Reading csv file with pandas')
    tp = pd.read_csv(file,
                     delimiter=',', 
                     header=0, 
                     chunksize=10000,
                     dtype={'user': int,
                            'venue': int, 
                            'point': list,
                            'time': datetime,
                            'cand_checked': list,
                            'cand_all': list})
    df = pd.concat(tp, ignore_index=True)
    return df


# In[26]:

# Path
path = '/Volumes/Tyr/Projects/UFMG/Datasets/Ours/NYC'
n_folds = 8

for i in range(1,n_folds+1):
    fold = '%s/fold_%d' % (path, i)
    file_test = '%s/test.txt' % fold
    file_validation = '%s/validation.txt' % fold
    
    #Validation
    if os.path.exists(file_validation):
        out_test = '%s/g_validation.trec' % fold
        data = load_data(file_validation)
        
        fo = open(out_test, 'w')
        for index, row in data.iterrows():
            query_id = 'Q' + str(index+1)
            item = str(row.venue)
            fo.write('%s\t0\t%s\t1\n' % (query_id, item))
        fo.close()
        
    #Test
    if os.path.exists(file_test):
        out_test = '%s/g_test.trec' % fold
        data = load_data(file_test)
        
        fo = open(out_test, 'w')
        for index, row in data.iterrows():
            query_id = 'Q' + str(index+1)
            item = str(row.venue)
            fo.write('%s\t0\t%s\t1\n' % (query_id, item))
        fo.close()

