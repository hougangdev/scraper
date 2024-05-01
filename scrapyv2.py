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

try:
    driver.get("https://www.niftygateway.com/rankings")
    
    # Wait for the 'Last 7 Days' button to be clickable
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="component-button"]'))
    )
    
    # Refetch and click the 'Last 7 Days' button
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/button/div')
    
    # ActionChains to perform human-like click
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()
    
    # Wait for AJAX or page updates as necessary
    WebDriverWait(driver, 100).until(
        lambda driver: driver.execute_script("return document.readyState") == 'complete'
    )
    
    # Wait for the table or rows to be visible
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.MuiTableRow-root"))
    )

    # Open CSV file to write the volumes
    with open('volumes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Fetch all elements
        elements = driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-8wlbod span")
        current_row = []

        # Iterate over elements to fill the rows
        for i, element in enumerate(elements):
            try:
                volume = element.text
                current_row.append(volume)  # Append data to the current row list
                if len(current_row) == 6:  # Check if the row has 6 columns filled
                    writer.writerow(current_row)
                    current_row = []  # Reset the current row list
            except StaleElementReferenceException:
                # Retry fetching the element in case of stale reference
                print("Stale element reference, retrying...")
                element = driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-8wlbod span")[i]
                volume = element.text
                current_row.append(volume)
                if len(current_row) == 6:
                    writer.writerow(current_row)
                    current_row = []

        # Handle any leftover items in case total number of elements isn't a perfect multiple of 6
        if current_row:
            writer.writerow(current_row)

finally:
    driver.quit()
