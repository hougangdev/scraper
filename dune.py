import pandas as pd
import os
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
import csv

# setting up
load_dotenv()
dune = DuneClient.from_env()

# dune query response
response = dune.get_latest_result(1933290)

filepath = 'output/7_day_volume.csv'

if response and response.result and response.result.rows:  # check if response is not empty
    result_rows = response.result.rows  
    fieldnames = response.result.metadata.column_names

    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_rows:
            writer.writerow(row)

    print(f"Data successfully written to {filepath}")

    # Load data from CSV
    df = pd.read_csv(filepath)

    # Convert 'volume' to integer for full number formatting
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    df.dropna(subset=['volume'], inplace=True)
    df['volume'] = df['volume'].astype(int)

    # Sort by 'volume' in descending order
    df = df.sort_values(by='volume', ascending=False)

    # Get the top 3 performing marketplaces
    top_three = df.head(3)

    # Format output
    print("Top 3 Performing Marketplaces:")
    print(top_three[['project', 'volume']].to_string(index=False, header=True))
else:
    print("No data available to write.")
