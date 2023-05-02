import numpy as np
import pandas as pd
import scipy
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

import sklearn
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from scipy.spatial import distance
from scipy import stats

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 100)



def t20_player_recommend(name):
    df = pd.read_csv('cricket_player_stats.csv')
    df = df.drop(columns = ['BT_Test_M',
       'BT_Test_Inn', 'BT_Test_NO', 'BT_Test_Runs', 'BT_Test_HS',
       'BT_Test_Avg', 'BT_Test_BF', 'BT_Test_SR', 'BT_Test_100', 'BT_Test_200',
       'BT_Test_50', 'BT_Test_4s', 'BT_Test_6s', 'BT_ODI_M', 'BT_ODI_Inn',
       'BT_ODI_NO', 'BT_ODI_Runs', 'BT_ODI_HS', 'BT_ODI_Avg', 'BT_ODI_BF',
       'BT_ODI_SR', 'BT_ODI_100', 'BT_ODI_200', 'BT_ODI_50', 'BT_ODI_4s',
       'BT_ODI_6s','BW_Test_M',
       'BW_Test_Inn', 'BW_Test_B', 'BW_Test_Runs', 'BW_Test_Wkts',
       'BW_Test_BBI', 'BW_Test_BBM', 'BW_Test_Econ', 'BW_Test_Avg',
       'BW_Test_SR', 'BW_Test_5W', 'BW_Test_10W', 'BW_ODI_M', 'BW_ODI_Inn',
       'BW_ODI_B', 'BW_ODI_Runs', 'BW_ODI_Wkts', 'BW_ODI_BBM', 'BW_ODI_Econ',
       'BW_ODI_Avg', 'BW_ODI_SR', 'BW_ODI_5W', 'BW_ODI_10W', ])
    df[['BT_T20I_Avg', 'BT_T20I_SR']] = df[['BT_T20I_Avg', 'BT_T20I_SR']].fillna(0)
    dobdf = df['date_of_birth'].str.extract(r'(\d{4})')
    dobdf = dobdf.fillna(0)
    df['year'] = dobdf.astype(int)
    df.drop(['Unnamed: 0', 'date_of_birth'],axis=1,inplace=True)
    df1 = df[df['year']>=1986]
    t20_cricket_playing_nations = ['Australia', 'England', 'Ireland','India', 'Pakistan', 'New Zealand', 'West Indies', 'South Africa', 'Sri Lanka', 'Afghanistan', 'Bangladesh', 'Zimbabwe']
    df1 = df1[df1['team'].isin(t20_cricket_playing_nations)]
    df = df1
    df = df.loc[(df['BT_T20I_M']> 0) | (df['BW_T20I_M']> 0)]
    def boundary_rate(player):
        num_of_fours = player['BT_T20I_4s']
        num_of_sixes = player['BT_T20I_6s']
        balls_faced = player['BT_T20I_BF']
        if (balls_faced > (num_of_fours + num_of_sixes)):
            return round((num_of_fours + num_of_sixes) / balls_faced, 3)
        else:
            return 0
    df['BT_T20I_BR'] = df.apply(lambda row: boundary_rate(row), axis=1)
    df2 = df[(np.abs(stats.zscore(df['BT_T20I_BR'])) > 3)]
    df2[["name", "year", "BT_T20I_M", "BT_T20I_Runs","team", "BT_T20I_BF", "BT_T20I_SR", "BT_T20I_BR"]]
    df.drop(df2.index,axis=0,inplace=True)
    tdf = df[['name', 'team', 'BT_T20I_M', 'BT_T20I_Inn', 'BT_T20I_NO',
       'BT_T20I_Runs', 'BT_T20I_HS', 'BT_T20I_Avg', 'BT_T20I_BF', 'BT_T20I_SR',
       'BT_T20I_100', 'BT_T20I_200', 'BT_T20I_50', 'BT_T20I_4s', 'BT_T20I_6s',
       'BW_T20I_M', 'BW_T20I_Inn', 'BW_T20I_B', 'BW_T20I_Runs', 'BW_T20I_Wkts',
       'BW_T20I_BBM', 'BW_T20I_Econ', 'BW_T20I_Avg', 'BW_T20I_SR',
       'BW_T20I_5W', 'BW_T20I_10W', 'BT_T20I_BR']]
    tdf.drop(['team'],axis=1,inplace=True)
    def conversion(str):
        if str != '0':
            try:
                l = str.split()
                l.remove('for')
                nl = [float(x) for x in l]
                k = nl[0]/nl[1]
                return k
            except:
                l = str.split()
                l.remove('for')
                nl = [float(x) for x in l]
                if nl[0] !=0:
                    return nl[0]
                else:
                    return 0
        else:
            return 0
    tdf['BW_T20I_BBM'] = tdf['BW_T20I_BBM'].apply(conversion)
    tdf['mor_cols'] = tdf['BT_T20I_NO']+ tdf['BT_T20I_Runs']+ tdf['BT_T20I_HS']+ tdf['BT_T20I_Avg']+\
                tdf['BT_T20I_SR'] + tdf['BT_T20I_100']+ tdf['BT_T20I_200']+ tdf['BT_T20I_50']+\
                tdf['BT_T20I_4s']+ tdf['BT_T20I_6s']+ tdf['BW_T20I_Wkts'] + tdf['BW_T20I_5W'] + tdf['BW_T20I_10W']+tdf['BT_T20I_BR']
    tdf['less_cols'] = tdf['BW_T20I_Runs'] + tdf['BW_T20I_Econ'] + tdf['BW_T20I_Avg'] + tdf['BW_T20I_SR']
    tdf['impact_col'] = np.sqrt(tdf['mor_cols']/tdf['less_cols'])
    df3 = tdf[(tdf['BT_T20I_Inn'] == 0) & (tdf['BW_T20I_Inn'] == 0)]
    tdf.drop(df3.index,axis=0,inplace=True)
    tdf = tdf.replace([np.inf,np.nan],100)
    tdf.drop(['mor_cols', 'less_cols'], axis=1, inplace=True)
    tdf_col = ['BT_T20I_NO', 'BT_T20I_Runs','BT_T20I_HS', 'BT_T20I_Avg', 
           'BT_T20I_BF', 'BT_T20I_SR', 'BT_T20I_100','BT_T20I_200', 
           'BT_T20I_50', 'BT_T20I_4s', 'BT_T20I_6s','BW_T20I_B', 
           'BW_T20I_Runs', 'BW_T20I_Wkts','BW_T20I_BBM', 'BW_T20I_Econ', 
           'BW_T20I_Avg', 'BW_T20I_SR','BW_T20I_5W', 'BW_T20I_10W', 'BT_T20I_BR', 'impact_col']
    kmeans = KMeans(n_clusters = 5, random_state = 8)
    tdf['cluster'] = kmeans.fit_predict(tdf[tdf_col])
    df_cl1 = tdf[tdf['cluster'] == 0]
    df_cl2 = tdf[tdf['cluster'] == 1]
    df_cl3 = tdf[tdf['cluster'] == 2]
    df_cl4 = tdf[tdf['cluster'] == 3]
    df_cl5 = tdf[tdf['cluster'] == 4]
    def get_df(name):
        for df in [df_cl1,df_cl2,df_cl3,df_cl4,df_cl5]:
            if any(np.isin(df.name.values,name) == True):
                return df
            else:
                pass
    def player_recommendation(name):
        recommendation = []
        r_df = get_df(name)
        a = r_df.loc[r_df['name'] == name][tdf_col]
        a = np.array(a)
        for num in r_df.index:
            b = r_df.loc[r_df.index == num][tdf_col]
            b = np.array(b)
            c = distance.euclidean(a,b)
            recommendation.append([r_df.loc[r_df.index == num]['name'],c])
            recommendation.sort(key = lambda a: a[1])
        return [recommendation[1][0].values[0], recommendation[2][0].values[0], recommendation[3][0].values[0], recommendation[4][0].values[0]]
    
    pl_list = player_recommendation(name)
    return pl_list


t20_player_recommend('Rohit Sharma')









