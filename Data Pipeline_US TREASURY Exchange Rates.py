import requests
import pandas as pd
import sqlite3 

# Extract Data From API
url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"
params = {
    "fields": "record_date,country_currency_desc,exchange_rate",
    "filter": "record_date:gte:2020-01-01"
}
response = requests.get(url, params=params)
data = response.json()
df = pd.DataFrame(data['data'])

# Transform Data
df_small = df[['record_date', 'country_currency_desc', 'exchange_rate']]
df_small.columns = df_small.columns.str.strip().str.lower().str.replace(' ', '_')
df_small['record_date'] = df['record_date'].fillna(0)
df_small['country_currency_desc'] = df['country_currency_desc'].fillna(0)
df_small['exchange_rate'] = df['exchange_rate'].fillna(0)

# Load Data into SQLite
conn = sqlite3.connect('exchange_rate.db')
df.to_sql('exchange_rate', conn, if_exists='replace', index=False)

#Ranking Currencies by Exchange Rate From Highest To Lowest
Desc_Query = """
SELECT 
    record_date, 
    country_currency_desc, 
    exchange_rate 
FROM exchange_rate 
ORDER BY exchange_rate DESC
"""
print(pd.read_sql(Desc_Query, conn))

#Finding How Many Currencies Have An Exchange Rate Below 1 (i.e., stronger than USD).
Exchange_Rate_Below_1_Query = """
SELECT 
    country_currency_desc, 
    exchange_rate,    
    COUNT(country_currency_desc) OVER () AS num_of_currency
FROM exchange_rate
WHERE exchange_rate < 1.0
ORDER BY exchange_rate ASC;
"""
print(pd.read_sql(Exchange_Rate_Below_1_Query, conn))
