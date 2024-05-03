import csv
import time
import os
import pandas as pd
import sys

# module path
nifty_module_path = 'utils'
sys.path.append(nifty_module_path)

# module imports
import nifty_scrap

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
from nifty_scrap import get_total_sales_volume

# dune setup
load_dotenv()
dune = DuneClient.from_env()

# abstract class for data providers
class DataProvider(ABC):
    name: str
    
    @property
    @abstractmethod
    def name(self) -> str:
        return "data-provider"
    
    @abstractmethod
    def get_7day_volume(self):
        # return 7 day volume as a float
        # ...
        pass
    
    @abstractmethod
    def get_royalties_earned(self):
        # return royalties earned as a float
        # ...
        pass

# concrete classes for marketplaces
class NiftyProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "nifty_gateway"
    
    def __init__(self):
        self._volume = None # initialise new volume as none
    
    def get_7day_volume(self):
        # fetch and store the volume only if it hasn't been retrieved before
        if self._volume is None:
            self._volume = get_total_sales_volume()
        return self._volume
    
    def get_royalties_earned(self):
        nifty_royalties = 0.05 * self._volume  # Calculate 5% of the sales volume
        return f"{nifty_royalties:.2f}"
        
        
class OpenseaProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "opensea"
    
    def get_7day_volume(self):
        response = dune.get_latest_result(1933290)
        if response and response.result and response.result.rows:
            try:
                # Find the 'OpenSea' entry and return its volume
                opensea_volume = next(row['volume'] for row in response.result.rows if row['project'] == 'OpenSea')
                return f"{opensea_volume:.2f}"
            except StopIteration:
                # Handle the case where 'OpenSea' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    
    def get_royalties_earned(self):
        response = dune.get_latest_result(2021068)
        if response and response.result and response.result.rows:
            try:
                # Find the 'OpenSea' entry and return its volume
                opensea_royalties = next(row['fees_paid'] for row in response.result.rows if row['name'] == 'OpenSea')
                return f"{opensea_royalties:.2f}"
            except StopIteration:
                # Handle the case where 'OpenSea' is not found
                return 0
        return 0  # Return 0 if there's no valid data

class BlurProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "blur"
    
    def get_7day_volume(self):
        response = dune.get_latest_result(1933290)
        if response and response.result and response.result.rows:
            try:
                blur_volume = next(row['volume'] for row in response.result.rows if row['project'] == 'Blur')
                return f"{blur_volume:.2f}"
            except StopIteration:
                # Handle the case where 'Blur' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    
    def get_royalties_earned(self):
        response = dune.get_latest_result(2021068)
        if response and response.result and response.result.rows:
            try:
                # Find the 'Blur' entry and return its volume
                blur_royalties = next(row['fees_paid'] for row in response.result.rows if row['name'] == 'Blur')
                return f"{blur_royalties:.2f}"
            except StopIteration:
                # Handle the case where 'Blur' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    
class MagicEdenProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "magic_eden"
    
    def get_7day_volume(self):
        response = dune.get_latest_result(1933290)
        if response and response.result and response.result.rows:
            try:
                magic_eden_volume = next(row['volume'] for row in response.result.rows if row['project'] == 'Magic Eden')
                return f"{magic_eden_volume:.2f}"
            except StopIteration:
                # Handle the case where 'Magic Eden' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    
    def get_royalties_earned(self):
        response = dune.get_latest_result(2021068)
        if response and response.result and response.result.rows:
            try:
                # Find the 'Magic Eden' entry and return its volume
                magic_eden_royalties = next(row['fees_paid'] for row in response.result.rows if row['name'] == 'Magic Eden')
                return f"{magic_eden_royalties:.2f}"
            except StopIteration:
                # Handle the case where 'Magic Eden' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    

# setting up the dataframe
data_providers = [
    NiftyProvider(),
    OpenseaProvider(),
    BlurProvider(),
    MagicEdenProvider(),
]

COLUMN_NAMES = ["project", "7_day_volume", "7_day_royalties"]

df = pd.DataFrame(columns=COLUMN_NAMES)

for provider in data_providers:
    # Get and format the 7-day volume
    volume = float(provider.get_7day_volume())  # Assuming get_7day_volume() returns a string that can be converted to float
    formatted_volume = f"{volume:.2f}"

    # Get and format the royalties
    royalties = float(provider.get_royalties_earned())  # Assuming get_royalties_earned() returns a string that can be converted to float
    formatted_royalties = f"{royalties:.2f}"

    # Append data to DataFrame using df.loc
    df.loc[len(df)] = [provider.name, formatted_volume, formatted_royalties]

print(df)

# date formatting
today = datetime.now()
seven_days_ago = today - timedelta(days=7)

start_date_str = seven_days_ago.strftime("%m%d")
end_date_str = today.strftime("%m%d")

# CSV writing
df.to_csv(f"output/{start_date_str}-{end_date_str}.csv", index=False)

if __name__ == "__main__":
    pass