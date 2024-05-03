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
        return "nifty"
    
    def get_7day_volume(self):
        #method implementation - selenium
        return 69.69
        
class OpenseaProvider(DataProvider):
    
    @property
    def name(self) -> str:
        return "open-sea"
    
    def get_7day_volume(self):
        #method implementation - dune
        return 111.11

data_providers = [
    NiftyProvider(),
    OpenseaProvider(),
]

# Setting up the dataframe
COLUMN_NAMES = ["project", "7_day_volume"]

df = pd.DataFrame(columns=COLUMN_NAMES)

for provider in data_providers:
    df.loc[len(df), df.columns] = [provider.name, provider.get_7day_volume()]

print(df)

df.to_csv("output/7day_volume.csv", index=False)