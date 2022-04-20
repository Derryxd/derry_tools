import os
import sys
import oss2
import yaml
import glob
import datetime
import itertools
import numpy as np
import pandas as pd
import datetime as dtm
import matplotlib.pyplot as plt

from metar import Metar
from ldz_tools.misc import *

def get_metar(content):
    obs = Metar.Metar(content)
    result = dict([string.split(': ') for string in obs.string().split('\n')])
    result['creat time'] = pd.to_datetime(result['time'])
    result['VIS'] = float(result['visibility'].split(' ')[0])
    result['T'] = float(result['temperature'].split(' ')[0])
    result['TD'] = float(result['dew point'].split(' ')[0])
    result['QNH'] = float(result['pressure'].split(' ')[0])
    result.pop('time')
    return result

def dump_airport_dataset(path='/data/model_online/vis_predict', 
                         ap='ZBAA', 
                         yrs=[2020], 
                         is_save=True,
                         path_save='/data/model_online/vis_predict/dataset',
                         col_t='OBSERVATION_TIME',
                         col_wea='WETHER',
                         var_lst=['VIS', 'WINDDIRECTION', 'WINDSPEED', 'T', 'TD', 'QNH']):
    df_save = pd.DataFrame()
    for yr in yrs:
        df_raw = pd.read_csv(os.path.join(path, f'data/metar_{ap}_{yr}.csv'))
        df_raw = indextime(df_raw, col_t)
        df_unique = df_raw.drop_duplicates(subset=[col_t, 'CONTENT'])
        df_unique.loc[df_unique[col_wea].isna(), col_wea] = 'MISSING'

        # train data
        df_var = df_unique[df_unique['TYPES']=='SA']
        df_var = df_var[~ (df_var == '--').any(axis=1)]
        df_var = df_var[~ (df_var == '///').any(axis=1)]
        df_var = df_var.drop_duplicates(subset=[col_t])
        df_var = df_var[[col_t, col_wea, 'TYPES'] + var_lst].dropna()
        df_var = df_var.set_index(col_t).resample('30min').asfreq().reset_index().dropna()
        df_var[var_lst] = df_var[var_lst].astype(float)
        
        # save 
        df_save = df_save.append(df_var)

    if is_save:
        os.system(f'mkdir -p {path_save}')
        df_save.to_csv(os.path.join(path_save, f'{ap}.csv'), index=False)    
    return df_save

# 获取机场data
from collections import Counter
def process_metar_vis(df, 
                      col_t='OBSERVATION_TIME',
                      listBins = [-1, 1000, 3000, 5000, 1000000],
                      listLabels = [1, 2, 3, 4]):
    # listBins = [-1, 800, 2000, 4000, 9001, 1000000]
    df = indextime(df, col_t)
    df['log_y'] = np.log(df['VIS'])
    df['level'] = pd.cut(df['VIS'], bins=listBins, labels=listLabels, include_lowest=True)
    df['month'] = [i for i in df[col_t].dt.month]
    # df['y'] = (df['log_y'] - df['log_y'].mean()) / (df['log_y'].std())
    a = Counter(df['level'])
    print('类别：', sorted(a.items(), key=lambda item:item[0]))
    return df

# 检测缺失情况
def get_nan_30min(df, time_col, freq='30min'):
    dd = df.set_index(time_col).resample(freq).asfreq()
    dd = dd[dd.isna().any(axis=1)].reset_index()
    dd['delta'] = [i.total_seconds()/60 for i in dd[time_col] - dd[time_col].shift(1)]
    return dd

def check_continuous(df, value_col, value):
    df['flag'] = np.where((df[value_col] == df[value_col].shift(1)) & (df[value_col] == value), 0, 1)
    df['flag_cumsum'] = df['flag'].cumsum()
    se_group = df.groupby(df['flag'].cumsum())['flag'].count()
    df['flag_count'] = df['flag_cumsum'].apply(lambda x: se_group.loc[x])
    a = Counter(df['flag_count'])
    print('缺失：', sorted(a.items(), key=lambda item:item[0]))
    return df

