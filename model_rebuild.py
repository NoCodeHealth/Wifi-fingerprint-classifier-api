import pandas as pd
import numpy as np
from key_biz import DATA_FILEPATH #private filepath
import matplotlib.pyplot as plt
import glob
import pickle
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score,accuracy_score,balanced_accuracy_score

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    

model = GradientBoostingClassifier()


def unique_adj(df,target='emptyScan'):
    if target in df.unique():
        return len(df.unique()) - 1
    else:
        return len(df.unique())

def emptyScan_count(df, target='emptyScan'):
    count = df.value_counts()
    return count.get('emptyScan',0)


def load_and_create_date(fp):

    temp_df = pd.read_csv(fp, index_col=None, header=0)
    temp_df = temp_df[['Device','H1','TS', 'BSSID', 'SSID', 'Level','indoorsState']]
    #create date col
    temp_df['date'] = pd.to_datetime(temp_df.TS,unit='ms')
    #deal with the emptyScan issue - create a new feature denoting emptyScan vs not, and remove emptyScan 'readings'
    temp_df['Level'] = np.where(temp_df['BSSID'] == 'emptyScan', -150, temp_df['Level'])
    return temp_df


def group_and_manip(df):
    tgroup = df.groupby(
        [
            pd.Grouper(key='date',freq='60s'),
            'indoorsState'
        ]
    ).agg(
        {
        'Level':['sum','mean','median','min','max','std'],
        'BSSID':[unique_adj, emptyScan_count, 'count']
    }
    ).reset_index()

    tgroup.columns = tgroup.columns.map('_'.join).str.strip('_')

    tgroup['max_diff'] = tgroup['Level_max'] - tgroup['Level_min']
    
    return tgroup


def proc(df_cat):
    df_nums = df_cat.drop(
            columns=['date','indoorsState']
            ).fillna(-130)

    X_train, X_test, y_train, y_test = train_test_split(
                                        df_nums,
                                        df_cat['indoorsState'],
                                        test_size=0.33
                                        )

    test_clf = model.fit(X_train,y_train) 
    preds = test_clf.predict(X_test)
    accuracy = balanced_accuracy_score(y_test, preds)
    f1 = f1_score(y_test,preds)

    print('running with approximate \nbalanced accuracy: {} and \nf1 score: {}'.format(accuracy,f1))
    print('retraining on all test data, for production')

    full_clf = model.fit(df_nums, df_cat['indoorsState'])
    return full_clf

def run():
    '''
    processes training data into production-ready model.
    Current balanced_accuracy_score result: 0.74369
    current f1_score result: 0.95202
    '''

    fp = DATA_FILEPATH
    fps = glob.glob(fp + '*.csv')
    fps = [f for f in fps if 'Log' not in f]

    allf = []
    for filepath in fps:
        df = load_and_create_date(filepath)
        grouped_df = group_and_manip(df)
        allf.append(grouped_df)
    df_cat = pd.concat(allf)
    clf = proc(df_cat)
    with open('trained_io_model.model', 'wb') as f:
        pickle.dump(clf,f)

if __name__=="__main__":
    run()

