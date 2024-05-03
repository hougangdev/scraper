import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def find_and_get_text(driver, css_selector, retry_count=3):
    for attempt in range(retry_count):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return element.text
        except (StaleElementReferenceException, NoSuchElementException) as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(1)
    raise Exception("Failed to retrieve element after multiple attempts.")

def fetch_data(driver):
    # set the URL to scrape
    print("Starting Web Scraping...")
    driver.get("https://www.niftygateway.com/rankings")
    
    # page navigation
    print("Navigating to the 'Last 7 Days' button...")
    WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button'))
    )
    
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button')
    
    ActionChains(driver).move_to_element(button).click().perform()
    
    time.sleep(10)  # Wait for AJAX loads
    
    WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[50]"))
    )
    rows = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr")
    
    return [{'volume': find_and_get_text(row, "td:nth-of-type(3)")} for row in rows]

def clean_and_sum_volume(volume_data):
    def extract_numeric(value):
        # Find the first occurrence of a numeric pattern including decimals
        match = re.search(r'\d+\.\d+', value)
        if match:
            return float(match.group())
        else:
            return 0.0  # return 0.0 if no numeric value is found, or handle this case as needed

    total = sum(extract_numeric(data['volume']) for data in volume_data)
    return total


def get_total_sales_volume():
    driver = initialize_driver()
    try:
        volume_data = fetch_data(driver)
        total_volume = clean_and_sum_volume(volume_data)
        print(f"Total Sales Volume: {total_volume}")
        return total_volume
    finally:
        driver.quit()

if __name__ == "__main__":
    get_total_sales_volume()
