import csv
import time
import os
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Selenium setup

# Dune setup
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

# concrete classes for marketplaces
class NiftyProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "nifty_gateway"
    
    def get_7day_volume(self):
        #method implementation - selenium
        return nifty_gateway_volume
        
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
                return opensea_volume
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
                return blur_volume
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
                return magic_eden_volume
            except StopIteration:
                # Handle the case where 'Magic Eden' is not found
                return 0
        return 0  # Return 0 if there's no valid data
    
class CryptoPunksProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "cryptopunks"
    
    def get_7day_volume(self):
        response = dune.get_latest_result(1933290)
        if response and response.result and response.result.rows:
            try:
                cryptopunks_volume = next(row['volume'] for row in response.result.rows if row['project'] == 'CryptoPunks')
                return cryptopunks_volume
            except StopIteration:
                # Handle the case where 'CryptoPunks' is not found
                return 0
        return 0  # Return 0 if there's no valid data

# Setting up the dataframe

data_providers = [
    NiftyProvider(),
    OpenseaProvider(),
    BlurProvider(),
    MagicEdenProvider(),
    CryptoPunksProvider()
]

COLUMN_NAMES = ["project", "7_day_volume"]

df = pd.DataFrame(columns=COLUMN_NAMES)

for provider in data_providers:
    df.loc[len(df), df.columns] = [provider.name, provider.get_7day_volume()]

print(df)

# CSV writing
# date formatting
today = datetime.now()
seven_days_ago = today - timedelta(days=7)

start_date_str = seven_days_ago.strftime("%m%d")
end_date_str = today.strftime("%m%d")

df.to_csv(f"output/{start_date_str}-{end_date_str}.csv", index=False)