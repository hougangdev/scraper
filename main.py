import csv
import time
import os
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

# set up Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# path to your ChromeDriver
service = Service(executable_path="/usr/local/bin/chromedriver")

# initialize the driver
driver = webdriver.Chrome(service=service, options=options)

def find_and_get_text(driver, css_selector):
    attempts = 0
    while attempts < 3:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return element.text
        except StaleElementReferenceException:
            print("Encountered a stale element, retrying...")
            attempts += 1
    raise Exception("Failed to retrieve element after multiple attempts.")

def clean_price(price):
    cleaned_price = price.replace("$", "").replace(",", "")
    return float(cleaned_price)

def read_and_clean_data(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        # read each row in the input csv, clean it, and write to output csv
        for row in reader:
            if row: # if row is not empty
                cleaned_price = clean_price(row[0])
                writer.writerow([cleaned_price])

# summing up all the values in the cleaned csv
def sum_volume(input_file):
    total_sum = 0
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row:  # ensure the row is not empty
                try:
                    total_sum += float(row[0])
                except ValueError:
                    print(f"Skipping invalid value: {row[0]}")
    return total_sum

try:
    driver.get("https://www.niftygateway.com/rankings")
    
    # wait for the 'Last 7 Days' button to be clickable
    WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button'))
    )
    
    time.sleep(5)
    
    # refetch and click the 'Last 7 Days' button
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button')
    ActionChains(driver).move_to_element(button).click().perform()
    
    # wait after clicking button
    time.sleep(15)
    
    # wait for AJAX or page updates as necessary
    WebDriverWait(driver, 300).until(
        lambda x: x.execute_script("return document.readyState") == 'complete'
    )
    
    # ensure the table is fully loaded and stable before continuing
    WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody"))
    )
    
    # rows = driver.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
    rows = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr")
    
    # Open CSV file to write the extracted values
    with open('output/volume.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Iterate through each row and get the text from the 3rd 'td'
        for row in rows:
            third_td_css = "td:nth-of-type(3) span"  # More specific CSS selector for the third 'td' span
            try:
                span_text = find_and_get_text(row, third_td_css)
                writer.writerow([span_text])
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
finally:
    driver.quit()



                
# specify input and output file name
input_csv_path = 'output/volume.csv'
output_csv_path = 'output/cleaned_volume.csv'

read_and_clean_data(input_csv_path, output_csv_path)


# Calculate the total sum from the cleaned CSV file
total_sales_volume = sum_volume(output_csv_path)
print(f"Total Sales Volume: {total_sales_volume}")



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
    
    filename_path = f'output/{start_date_str}-{end_date_str}.csv'

    fieldnames = response.result.metadata.column_names

    with open(filename_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_rows:
            writer.writerow(row)
        writer.writerow({fieldnames[0]: "Nifty Gateway", fieldnames[1]: total_sales_volume})

    print(f"Data successfully written to {filename_path}")
else:
    print("No data available to write.")
