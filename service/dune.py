from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
import csv
import os
from datetime import datetime, timedelta

# setting up
load_dotenv()
dune = DuneClient.from_env()

# dune query response
response = dune.get_latest_result(1933290)

# date formatting
today = datetime.now()
seven_days_ago = today - timedelta(days=7)

start_date_str = seven_days_ago.strftime("%m%d")
end_date_str = today.strftime("%m%d")

if response and response.result and response.result.rows: #check if response is not empty
    result_rows = response.result.rows  
    
    filename = f'{start_date_str}-{end_date_str}.csv'

    fieldnames = response.result.metadata.column_names

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_rows:
            writer.writerow(row)

    print(f"Data successfully written to {filename}")
else:
    print("No data available to write.")
