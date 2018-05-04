"""
Date Written: 05/02/2018
Date Last Modefied: 05/03/2018
Author: Mohammad Aziz Moiuddin
Last Updated By: Mohammad Aziz Moiuddin
Code Description:
1. Import trades.csv to pandas dataframe
2. Write code to answer Python questions
"""

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from datetime import datetime

#Send output to file
curr_code_name = os.path.basename(__file__)
curr_file_name = curr_code_name.split('.py')[0]
ff = open(curr_file_name+'_log.txt','w')
sys.stdout = ff

#Import trades.csv into Python dataframe
df = pd.read_csv("trades.csv")

##### Question1
#Fetch all trades data and remove any data point which has holes (missing a column value).
#Compute the weighted average yeilds (weights are defined by ```par_traded``` value) and the sum of par_traded value for each individual cusip.
df = df.dropna()
df_wt_avg = pd.DataFrame(columns=['wavg_yield'])
df_wt_avg['wavg_yield'] = (df['yield']*df['par_traded']).groupby(df['cusip']).sum()/df['par_traded'].groupby(df['cusip']).sum()
print(df_wt_avg.head(10),'\n')


##### Question2
#Use the dataset from Question1 and define a bucket set as the following ```[round(-1+min(wavg_yield)), 0, 1, 2, 3, 4, 5, round(1+max(wavg_yield))]``` while the bucket edges are in the above list. Calculate the number of cusips that falls in each bucket.
list_bucket = [(round(-1+min(df_wt_avg['wavg_yield'])))] + list(map(lambda x: x, range(6))) + [(round(1+max(df_wt_avg['wavg_yield'])))]
df_wt_avg['bucket_wavg_yield'] = pd.cut(df_wt_avg['wavg_yield'], list_bucket)
df_cnt_cusip = pd.DataFrame(columns=['cnt_cusip'])
df_cnt_cusip['cnt_cusip'] = df_wt_avg.groupby(['bucket_wavg_yield'])['wavg_yield'].count()
print(df_cnt_cusip.head(10),'\n')


##### Question3
#Fetch all trades which settled on 2017-12-29 and remove any data point which has holes. Compute the weighted average yields (weights are defined by ```par_traded``` value) across all cusips for each individual maturity_date.
df_filtered = df[df['settlement_date'] == '2017-12-29']
lst_group_by = ['cusip', 'maturity_date']
df_filtered['temp'] = df_filtered['yield']*df_filtered['par_traded'] #temporary column to calculate product of yield and par_traded
df_filtered_wt_avg = pd.DataFrame(columns=['wavg_yield'])
df_filtered_wt_avg['wavg_yield'] = df_filtered.groupby(lst_group_by)['temp'].sum() / df_filtered.groupby(lst_group_by)['par_traded'].sum()
print(df_filtered_wt_avg.head(10), '\n')


##### Question4
#Use the dataset from Question3 and fit a curve for the function ```yield=f(maturity_date)```. Choose any model as you see fit.
#Add a column for numeric value of maturity_date
df_filtered['maturity_date_num'] = pd.to_datetime(df['maturity_date'])
#Shuffle datframe and split into training and test
X_train, X_test, y_train, y_test = train_test_split(df_filtered['maturity_date_num'], df_filtered['yield'], test_size=0.70, random_state=66, shuffle=True)
X_train = X_train.values.reshape(-1,1)
X_test = X_test.values.reshape(-1,1)
#Define GBM estimator
GBM_params = {'n_estimators': 100, 'max_depth': 2, 'min_samples_split': 2, 'learning_rate': 0.01, 'loss': 'ls'}
GBM = GradientBoostingRegressor(**GBM_params)
#Develop GBM on train and apply on test; show MSE on train and test
GBM.fit(X_train, y_train)
mse_train = mean_squared_error(y_train, GBM.predict(X_train))
mse_test = mean_squared_error(y_test, GBM.predict(X_test))
print("MSE Train: %.4f" % mse_train)
print("MSE Test: %.4f" % mse_test)
ff.close()
