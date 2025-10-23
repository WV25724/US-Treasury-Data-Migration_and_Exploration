import requests
import pandas as pd
import sqlite3 
import json

#Extract Currency Exchange Data From API
cur_ex_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"
cur_ex_params = {
    "fields": "record_date,country_currency_desc,exchange_rate",
    "filter": "record_date:gte:2020-01-01"
}
cur_ex_response = requests.get(cur_ex_url, params=cur_ex_params)
cur_ex_data = cur_ex_response.json()
cur_ex_df = pd.DataFrame(cur_ex_data["data"])

#Extract Debt to Penny Data from API
d2p_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"
d2p_params = {
    "fields": "record_date,tot_pub_debt_out_amt,record_fiscal_quarter",
    "filter": "record_date:gte:2020-01-01"
}
d2p_response = requests.get(d2p_url, params=d2p_params)
d2p_data = d2p_response.json()
d2p_df = pd.DataFrame(d2p_data["data"])

#Transform Data
#Select Relevant Columns
cur_ex_df_small = cur_ex_df[['record_date', 'country_currency_desc', 'exchange_rate']]

#Clean Column names
cur_ex_df_small.columns = cur_ex_df_small.columns.str.strip().str.lower().str.replace(' ', '_')

#Fill Missing Values with '0'
cur_ex_df_small['record_date'] = cur_ex_df['record_date'].fillna(0)
cur_ex_df_small['country_currency_desc'] = cur_ex_df['country_currency_desc'].fillna(0)
cur_ex_df_small['exchange_rate'] = cur_ex_df['exchange_rate'].fillna(0)

#Select Relevant Columns
d2p_df_small = d2p_df[['record_date', 'tot_pub_debt_out_amt', 'record_fiscal_quarter']]

#Rename Selected Column
d2p_df_small.rename(columns={'tot_pub_debt_out_amt': 'total_public_debt'}, inplace=True)

#Fill Missing Values with '0'
d2p_df_small.columns = d2p_df_small.columns.str.strip().str.lower().str.replace(' ', '_')

#Fill Missing Values with '0'
d2p_df_small['record_date'] = d2p_df['record_date'].fillna(0)
d2p_df_small['total_public_debt'] = d2p_df['tot_pub_debt_out_amt'].fillna(0)
d2p_df_small['record_fiscal_quarter'] = d2p_df['record_fiscal_quarter'].fillna(0)

#Load Data into SQLite
conn = sqlite3.connect('exchange_rate.db')
df.to_sql('exchange_rate', conn, if_exists='replace', index=False)
# 
# #Ranking Currencies by Exchange Rate From Highest To Lowest
# Desc_Query = """
# SELECT 
#     record_date, 
#     country_currency_desc, 
#     exchange_rate 
# FROM exchange_rate 
# ORDER BY exchange_rate DESC
# """
# print(pd.read_sql(Desc_Query, conn))
# 
# #Finding How Many Currencies Have An Exchange Rate Below 1 (i.e., stronger than USD).
# Exchange_Rate_Below_1_Query = """
# SELECT 
#     country_currency_desc, 
#     exchange_rate,    
#     COUNT(country_currency_desc) OVER () AS num_of_currency
# FROM exchange_rate
# WHERE exchange_rate < 1.0
# ORDER BY exchange_rate ASC;
# """
# print(pd.read_sql(Exchange_Rate_Below_1_Query, conn))
