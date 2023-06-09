# -*- coding: utf-8 -*-
"""test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1meNH3LR29drd4wONqyYUfF-oKaEbXbq4
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import sklearn
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from scipy.spatial import distance
from scipy import stats

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 100)

df = pd.read_csv('cricket_player_stats.csv')

df.head()

df.isna().sum().max()

nans = df[df.isna().any(axis=1)]
nans

df[['BW_Test_Avg', 'BW_Test_SR']] = df[['BW_Test_Avg', 'BW_Test_SR']].fillna(0)

df.isna().sum().max()

mdf = df['date_of_birth'].str.extract(r'(\d{4})')

mdf = mdf.fillna(0)
mdf.tail()

df['year'] = mdf.astype(int)

df.head()

df.columns

df.drop(['Unnamed: 0','date_of_birth'],axis=1,inplace=True)

df.head()

final_df = df[df['year']>=1986]

final_df.tail()

final_df.shape

final_df.info()

print(f'Rows in DataFrame before split: {final_df.shape[0]}')
test_cricket_playing_nations = ['Australia', 'England', 'Ireland','India', 'Pakistan', 'New Zealand', 'West Indies', 'South Africa', 'Sri Lanka', 'Afghanistan', 'Bangladesh', 'Zimbabwe']
final_df = final_df[final_df['team'].isin(test_cricket_playing_nations)]
print(f'Rows in DataFrame after split: {final_df.shape[0]}')

df = final_df

df.head()

df = df.loc[(df['BT_Test_M']> 0) | (df['BT_ODI_M'] > 0) | (df['BT_T20I_M'] > 0) | (df['BW_Test_M']> 0) | (df['BW_ODI_M'] > 0) | (df['BW_T20I_M'] > 0)]

df.shape

df['BT_Test_SR'].describe()

def boundary_rate(player):
    num_of_fours = player["BT_Test_4s"]
    num_of_sixes = player["BT_Test_6s"]
    balls_faced = player["BT_Test_BF"]
    if (balls_faced > (num_of_fours + num_of_sixes)):
        return round((num_of_fours + num_of_sixes) / balls_faced, 3)
    else:
        return 0
    
df['BT_Test_BR'] = df.apply(lambda row: boundary_rate(row), axis=1)

# plt.figure(figsize=(10,2))
# p1 = sns.boxplot(data=df, x='BT_Test_BR')
# p1.set(title='Boundary Rate Distribution')
# plt.show()

temp_df = df[(np.abs(stats.zscore(df['BT_Test_BR'])) > 3)]
print(temp_df.shape)
temp_df[["name", "year", "BT_Test_M", "BT_Test_Runs","team", "BT_Test_BF", "BT_Test_SR", "BT_Test_BR"]].sort_values("BT_Test_BR", ascending=False).head(20)

# plt.figure(figsize=(15,8))
# p1 = sns.histplot(data=df, x='team', hue='team', legend=True)
# p1.set(title='Number of Players - Country-wise')
# plt.show()

df.head()

df.columns

t_df = df[['name', 'team', 'BT_Test_M', 'BT_Test_Inn', 'BT_Test_NO',
       'BT_Test_Runs', 'BT_Test_HS', 'BT_Test_Avg', 'BT_Test_BF', 'BT_Test_SR',
       'BT_Test_100', 'BT_Test_200', 'BT_Test_50', 'BT_Test_4s', 'BT_Test_6s','BW_Test_M', 'BW_Test_Inn', 'BW_Test_B', 'BW_Test_Runs',
       'BW_Test_Wkts', 'BW_Test_BBI', 'BW_Test_BBM', 'BW_Test_Econ',
       'BW_Test_Avg', 'BW_Test_SR', 'BW_Test_5W', 'BW_Test_10W','BT_Test_BR']]

t_df

team_df = t_df.copy()

t_df.drop(['team'],axis=1,inplace=True)

t_df.head()

s = '3 for 10'
l = s.split()
l.remove('for')
l
nl = [float(x) for x in l]
k = nl[0]/nl[1]
k

def conv_num(st):
    if st !='0':
        try:    
            l = st.split()
            l.remove('for')
            nl = [float(x) for x in l]
            k = nl[0]/nl[1]
            return k
        except:
            l = st.split()
            l.remove('for')
            nl = [float(x) for x in l]
            if nl[0] != 0:
                return nl[0]
            else:
                return 0
            
    else:
        return 0

t_df['BW_Test_BBI'] = t_df['BW_Test_BBI'].apply(conv_num)
t_df['BW_Test_BBM'] = t_df['BW_Test_BBM'].apply(conv_num)

t_df.head()

t_df.shape

t_df['mor_col'] = t_df['BT_Test_NO']+ t_df['BT_Test_Runs']+ t_df['BT_Test_HS']+ t_df['BT_Test_Avg']+\
                t_df['BT_Test_SR'] + t_df['BT_Test_100']+ t_df['BT_Test_200']+ t_df['BT_Test_50']+\
                t_df['BT_Test_4s']+ t_df['BT_Test_6s']+ t_df['BT_Test_BR'] +\
                t_df['BW_Test_Wkts']  + t_df['BW_Test_BBI'] + t_df['BW_Test_5W'] + t_df['BW_Test_10W']

t_df['les_col'] =   t_df['BW_Test_Runs'] + t_df['BW_Test_Econ']+ t_df['BW_Test_Avg'] + t_df['BW_Test_SR']

t_df['impact_col'] = np.sqrt(t_df['mor_col']/t_df['les_col'])

t_df.head()

subset_df = t_df[(t_df['BT_Test_Inn'] == 0) & (t_df['BW_Test_Inn'] == 0)]

subset_df

t_df.drop(subset_df.index,axis=0,inplace=True)

t_df

t_df = t_df.replace([np.inf,np.nan],100)

t_df

t_df.drop(['mor_col','les_col'],axis=1,inplace=True)

t_df.columns

t_df_col = ['BT_Test_NO', 'BT_Test_Runs','BT_Test_HS', 'BT_Test_Avg', 'BT_Test_SR', 'BT_Test_100',
       'BT_Test_200', 'BT_Test_50', 'BT_Test_4s', 'BT_Test_6s', 'BW_Test_Runs', 'BW_Test_Wkts',
       'BW_Test_BBI', 'BW_Test_BBM', 'BW_Test_Econ', 'BW_Test_Avg','BW_Test_SR', 'BW_Test_5W', 'BW_Test_10W', 
       'BT_Test_BR', 'impact_col']

t_df.isna().sum().max()

t_df = t_df[~t_df['name'].isin(['Aaron Finch','Eoin Morgan','Pragyan Ojha','Piyush Chawla','Karn Sharma','Cheteshwar Pujara','Sudeep Tyagi',
                                'Saurabh Tiwary','Abhimanyu Mithun','Rahul Sharma',
                                'Suresh Raina'])]

nam = list(t_df.name)
test_players = sorted(nam)
test_players

def min_max_scaling(ser):
    return (ser - ser.min()) / (ser.max() - ser.min())

for col in t_df_col:
    t_df[col] = min_max_scaling(t_df[col])

from sklearn.cluster import KMeans

inertia = []
for n in range(1,15):
    kmeans = KMeans(n_clusters = n, random_state=7)
    kmeans.fit(t_df[t_df_col])
    inertia.append(kmeans.inertia_)

# plt.figure(figsize = (12,8))
# plt.plot(range(1,15),inertia)
# plt.title('Inertia scores')
# plt.show()

kmeans = KMeans(n_clusters = 5, random_state=7)
t_df['cluster'] = kmeans.fit_predict(t_df[t_df_col])

t_df.head()

t_df.cluster.value_counts()

df1 = t_df[t_df['cluster'] == 0]
df2 = t_df[t_df['cluster'] == 1]
df3 = t_df[t_df['cluster'] == 2]
df4 = t_df[t_df['cluster'] == 3]
df5 = t_df[t_df['cluster'] == 4]

def get_df(name):

    for df in [df1, df2, df3, df4, df5]:
        if any(np.isin(df.name.values,name) == True):
            return df
        else:
            pass

     
def player_recommendation(name,method=''):
    recommendation = []
    r_df = get_df(name)
    a = r_df.loc[r_df['name']==name][t_df_col]
    a = np.array(a)
    for num in r_df.index:
        b = r_df.loc[r_df.index==num][t_df_col]
        b = np.array(b)
        c = distance.euclidean(a,b)
        recommendation.append([r_df.loc[r_df.index==num]['name'],c])
        recommendation.sort(key=lambda a: a[1])
    return [recommendation[1][0].values[0],recommendation[2][0].values[0],recommendation[3][0].values[0],recommendation[4][0].values[0]]

player_recommendation('Virat Kohli')

player_recommendation('Jasprit Bumrah')

def player_team_recommendation(name):
    recommendations = []
    r_df = get_df(name)
    a = r_df.loc[r_df['name'] == name][t_df_col].values
    for _, row in r_df.iterrows():
        if row['name'] != name:
            b = row[t_df_col].values
            c = distance.euclidean(a,b)
            recommendations.append([row['name'],c])
    recommendations.sort(key=lambda x: x[1])
    return [rec[0] for rec in recommendations]

player_team_recommendation('Jasprit Bumrah')

def player_in_team(name):
    sim_players = player_team_recommendation(name)
    team = team_df.loc[team_df['name'] == name,'team'].iloc[0]
    sim_players_same_team = team_df.loc[(team_df['name'].isin(sim_players)) & (team_df['team'] == team), 'name'].tolist()
    return sim_players_same_team
    
player_in_team('Virat Kohli')



pl_list = ['Rohit Sharma','David Warner','Steven Smith','Virat Kohli','Ben Stokes','Ravindra Jadeja',
           'Ravichandran Ashwin','Tom Latham','Mohammed Siraj','Pat Cummins','Kagiso Rabada']

def team_recom(pl_list):
    opp_list = []

    for x in pl_list:
        new_pls = player_recommendation(x)
        if ((new_pls[0] not in opp_list) and (new_pls[0] not in pl_list)):
            opp_list.append(new_pls[0])
        elif ((new_pls[1] not in opp_list) and (new_pls[1] not in pl_list)):
            opp_list.append(new_pls[1])
        elif ((new_pls[2] not in opp_list) and (new_pls[2] not in pl_list)):
            opp_list.append(new_pls[2])
        else:
            opp_list.append(new_pls[3])
    return opp_list



team_recom(pl_list=pl_list)