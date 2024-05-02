import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Set up Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
service = Service(executable_path="/usr/local/bin/chromedriver")

# Initialize the driver
driver = webdriver.Chrome(service=service, options=options)

def find_and_get_text(driver, css_selector):
    # Attempt to find the element and get its text, retrying on StaleElementReferenceException
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

try:
    driver.get("https://www.niftygateway.com/rankings")
    
    # Wait for the 'Last 7 Days' button to be clickable
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="component-button"]'))
    )
    
    # Refetch and click the 'Last 7 Days' button
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button/div')
    ActionChains(driver).move_to_element(button).click().perform()
    
    # Wait for AJAX or page updates as necessary
    WebDriverWait(driver, 300).until(
        lambda x: x.execute_script("return document.readyState") == 'complete'
    )
    
    # Ensure the table is fully loaded and stable before continuing
    WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody"))
    )
    
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
    
    # Open CSV file to write the extracted values
    with open('output.csv', 'w', newline='') as file:
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
