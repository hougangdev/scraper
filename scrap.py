import time
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
     
    # for button in buttons:
    #     if "Last 7 Days" in button.text:
    #         # Using JavaScript to click to avoid StaleElementReferenceException
    #         driver.execute_script("arguments[0].click();", button)
    #         break
    
    # time.sleep(10)
    
    # Wait for AJAX or page updates as necessary
    WebDriverWait(driver, 100).until(
        lambda driver: driver.execute_script("return document.readyState") == 'complete'
    )
    
    WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "css-8wlbod"))
    )

    # Get the number of elements to handle
    num_elements = len(driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-8wlbod span"))

    # Iterate using index and refetch each time to avoid staleness
    for i in range(num_elements):
        try:
            # Refetching the elements in each iteration to avoid staleness
            element = driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-8wlbod span")[i]
            volume = element.text
            print(volume)
        except StaleElementReferenceException:
            print("Stale element reference, retrying...")
            element = driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-8wlbod span")[i]
            volume = element.text
            print(volume)

finally:
    driver.quit()
