"""
Date Written: 05/02/2018
Date Last Modefied: 05/03/2018
Author: Mohammad Aziz Moiuddin
Last Updated By: Mohammad Aziz Moiuddin
Code Description:
1. Code to convert trades.csv to SQL DB
2. Execute queries for SQL questions
"""

import pandas as pd
import sqlite3

## Problem Definition
#The ```trades.csv``` file contains a chunk of historical trade data for some muni bonds. The first row of the file is the header. There are 1000 records in this file.
#Write code in any language to load the file into a database table (preferable using in memeory database such as sqlite) and finish the following SQL questions. You can also load the code into a local database.
df = pd.read_csv("trades.csv")
conn = sqlite3.connect('trades.db')
df.to_sql('data', conn, flavor='sqlite', if_exists='replace', index=False)

cursor=conn.cursor()
### SQL
##### Question1
#Find the sum of ```par_traded``` value and the count of the trades for each cusip. Sort the result using the sum value from high to low then count value from low to high.
sql_query1 = 'DROP TABLE IF EXISTS SQL_Q1'
sql_query2 = 'CREATE TABLE SQL_Q1 AS SELECT cusip, sum(par_traded) as sum_par_traded, count(*) as num_trades FROM data GROUP BY cusip ORDER BY sum_par_traded DESC, num_trades'
cursor.execute(sql_query1)
cursor.execute(sql_query2)

### SQL
##### Question2
#Find the weighted average of yield for each cusip. The weights are ```par_traded``` value. Sort the result by the ```weighted_yield``` from high to low.
sql_query1 = 'DROP TABLE IF EXISTS SQL_Q2'
sql_query2 = 'CREATE TABLE SQL_Q2 AS SELECT cusip, sum(case when yield is not null then yield*par_traded end)/sum(case when yield is not null then par_traded end) as weighted_yield FROM data GROUP BY cusip ORDER BY weighted_yield DESC'
cursor.execute(sql_query1)
cursor.execute(sql_query2)

### SQL
##### Question3
#Find all ```settment_date``` while there were at least 5 or more unique cusips settled on the day. Return the ```settlement_date``` along with the count of unique cusips. Sort the result by the ```count``` from high to low.
sql_query1 = 'DROP TABLE IF EXISTS SQL_Q3'
sql_query2 = 'CREATE TABLE SQL_Q3 AS SELECT settlement_date, count(distinct cusip) as count_unique_cusips FROM data GROUP BY settlement_date HAVING count_unique_cusips >= 5 ORDER BY count_unique_cusips DESC'
cursor.execute(sql_query1)
cursor.execute(sql_query2)

conn.close()
