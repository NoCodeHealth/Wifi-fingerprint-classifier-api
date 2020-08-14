import pandas as pd
import numpy as np

    
def unique_adj(df,target='emptyScan'):
    if target in df.unique():
        return len(df.unique()) - 1
    else:
        return len(df.unique())
def emptyScan_count(df, target='emptyScan'):
    count = df.value_counts()
    return count.get('emptyScan',0)

def process_input(input_json):
    """
    input:
        input_json:
            [
                {
                    "TS": int (ms timestamp), 
                    "BSSID": str (hex mac address),
                    "Level" float (wifi signal level)
                },
                ...
            ]
    """
    df = pd.DataFrame(input_json)
    #deal with the emptyScan issue - 
    #create a new feature denoting emptyScan vs not, and remove emptyScan 'readings'
    df['Level'] = np.where(df['BSSID'] == 'emptyScan', -150, df['Level'])
    #create dummy to group on - is there a better way to make a flat row from a
    #df?
    df['dummy_label'] = 'dummy'

    tgroup = df.groupby(
        'dummy_label'
        ).agg(
            {
                'Level':['sum','mean','median','min','max','std'],
                'BSSID':[unique_adj, emptyScan_count, 'count']
            }
        ).reset_index()

    tgroup.columns = tgroup.columns.map('_'.join).str.strip('_')
    tgroup['max_diff'] = tgroup['Level_max'] - tgroup['Level_min']  
    df_nums = tgroup.drop(columns=['dummy_label']).fillna(-150)

    return df_nums.values
