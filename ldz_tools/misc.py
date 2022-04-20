import os
import yaml 
import pandas as pd

def dfread(path, is_csv=True):
    if is_csv:
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    return df

def indextime(df, col='datetime'):
    df.loc[:, col] = pd.DatetimeIndex(df.loc[:, col])
    return df

def dfmerge(df_lst, on=None, index=False, how='inner'):
    if on is None:
        pass
    elif isinstance(on, str):
        on = [on]
    elif isinstance(on, list):
        on = on
    else:
        raise IOError('Input "on" should be str or list.')
    df = df_lst[0]
    for df_tmp in df_lst[1:]:
        if not index:
            df = df.merge(df_tmp, on=on, how=how)
        else:
            df = df.merge(df_tmp, left_index=True, right_index=True, how=how)
    return df

def dfplot(df, time_col, cols_lst=None, title=None, leng=100, heig=8, y=None):
    if cols_lst is None:
        ax = df.set_index(time_col).plot(secondary_y=y, figsize=(leng, heig))
    else:
        ax = df.set_index(time_col)[cols_lst].plot(secondary_y=y, figsize=(leng, heig))
    if title is not None:
        plt.title(title, fontsize=30)
    return ax

def dump_yaml(path_yaml, obj_yaml):
    with open(path_yaml, "w", encoding="utf-8") as f:
        yaml.dump(obj_yaml, 
                  f, 
                  allow_unicode=True, 
                  default_flow_style=False, 
                  sort_keys=False)

def load_yaml(path_yaml):
    with open(path_yaml, "r", encoding="utf-8") as f:
        yaml_object = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_object


