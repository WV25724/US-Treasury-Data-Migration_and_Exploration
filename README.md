# ETL-Learning-Project-US-Treasury-Exchange-Rate
This project is a hands-on ETL (Extract, Transform, Load) learning exercise using the U.S. Treasury Exchange Rate API. It demonstrates how to collect exchange rate data, process it for analysis, and load it into a structured database for further use.
This project was created to consolidate understanding of ETL (Extract, Transform, Load) and extend that knowledge by learning how to:
  1. Extract financial data from a web API (U.S. Treasury Fiscal Data).
  2. Transform the raw JSON into a clean, tabular format.
  3. Load the processed data into an SQL database for queries and analysis.

The tools used for this project were
  1. Python 3.x
  2. Requests – to connect with the API and retrieve JSON data.
  3. Pandas – for cleaning and transforming the dataset.
  4. SQLite – as the target SQL database for storage and querying.

Screenshot of code:
<img width="1159" height="550" alt="Screeenshot for github" src="https://github.com/user-attachments/assets/7a4919e1-39ec-4f7e-9578-654feb736a4c" />

Why use SQLite?
- There are two reasons I chose to use SQLite instead of other database management systems
- 1. SQLite is portable and serverless. Since I was the sole user making changes to a local database, a full database server was unnecessary
- 2. Pandas has builtin support for SQLite via sqlite3, making it easier to read and write to a database directly. This allowed me to focus on the concepts behind data migration

