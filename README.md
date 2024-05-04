# Scraper Project

This project is a web scraping tool designed to extract data from websites. It uses Python and can be customized to scrape different types of data based on user requirements.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)

## Set Up

Follow these steps to set up the project locally:

### Python Set Up

1. **Clone the Repository**

   ```bash
   git clone https://github.com/hougangdev/scraper.git
   ```

2. **Create the Virtual Environment**

   ```python
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   ```bash
   source venv/bin/activate
   ```

4. **Install Python Modules**

   ```bash
   pip install -r requirements.txt
   ```

### Selenium Requirements

1. **Getting Chrome Driver**

   ```
   wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip
   ```

   Note:  
   Check this link for compatible ChromeDriver  
   `https://googlechromelabs.github.io/chrome-for-testing/#stable`

2. **Extracting Downloaded File:**

   ```bash
   unzip chromedriver-linux64.zip
   ```

   If `unzip` not installed, you can install it using `sudo apt install unzip`

3. **Make ChromeDriver Executable**

   ```bash
   chmod +x chromedriver
   ```

4. **Move ChromeDriver to a Directory in your PATH**

   ```bash
   sudo mv chromedriver /usr/local/bin/
   ```

5. **Verify ChromeDriver Installation**

   ```bash
   chromedriver --version
   ```

### .env

```
# Required
DUNE_API_KEY= abcdefghijklmnopqrstuvwxyz
```

## Running the Project

Ensure that .env has dune api key!

1. **Start Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
2. **Run dune.py**
   ```bash
   python3 dune.py
   ```
3. **Run main.py**
   ```bash
   python3 main.py
   ```

## Methodology

## Maintenance and Updates

Maintain the scraper by regularly updating the Python dependencies to mitigate security risks and ensure compatibility. Use pip to upgrade packages:

```bash
pip install --upgrade package-name
```

source venv/bin/activate
