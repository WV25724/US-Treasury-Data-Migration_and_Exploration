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
query = "SELECT record_date, country_currency_desc, exchange_rate FROM exchange_rate ORDER BY exchange_rate DESC LIMIT 5"
print(pd.read_sql(query, conn))
conn.close()
