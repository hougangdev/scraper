# Scraper Project

This project is a web scraping tool designed to extract data from websites. It uses Python and can be customized to scrape different types of data based on user requirements.

<p align="center">•
  <a href="#setup">Set Up</a> •
  <a href="#start">Start</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#maintenance">Maintenance and Updates</a> •
  <a href="#license">License</a> •
</p>

<div id="setup">

## Set Up

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)

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

</div>

<div id="start">

## Start

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

</div>

<div id="methodology">

## Methodology

### Choice of Dune Analytics for Onchain Data

For assessing the performance of NFT marketplaces that primarily transact onchain, I have selected [Dune Analytics](https://dune.com) as the primary data source. This decision was driven by the reliability and comprehensiveness of onchain data, which is considered the most accurate and tamper-proof source of information for blockchain transactions. Dune Analytics provides direct access to this data, enabling precise and real-time analysis of marketplace activity.

Dune Query No: 1933290, 2021068

### Web Scraping Nifty Gateway with Selenium

For the Nifty Gateway platform, which primarily handles transactions via credit card rather than onchain methods, a different approach was required. I have chosen to use Selenium for web scraping to gather data directly from the website. Given the dynamic nature of Nifty Gateway's web pages and the need to interact with JavaScript elements effectively, Selenium was chosen for its robust capabilities in handling such complexities. The use of a non-headless browser was necessary to ensure full loading of JavaScript-rendered content, which is essential for accessing accurate and complete data from the platform.

### Selection of Performance Metrics: Volume and Royalties

To evaluate the performance of various NFT marketplaces, I have decided to focuse on two key metrics: transaction volume and royalties earned. These metrics were chosen because they provide a clear indication of both the economic activity and the financial health of the artists and creators involved in the marketplace. Volume gives a measure of overall market activity and liquidity, while royalties reflect the ongoing benefits accruing to original creators, highlighting the sustainability and creator-friendliness of the marketplace.

### Implementation in Python Scripts

`dune.py`: This script interfaces with Dune Analytics through their API to fetch relevant onchain data about NFT marketplaces. The script filters and narrows down the list of marketplaces based on predefined criteria to identify those with significant activity and potential for in-depth analysis. It also includes functionality to export this data to CSV files for further analysis or reporting.

`main.py`: This script combines the data extracted from Nifty Gateway via Selenium with the onchain data obtained from Dune Analytics. The integration of these data sources in a single script allows for a comprehensive comparison across different types of NFT marketplaces. The combined data is then processed and exported to CSV format, facilitating easy access and manipulation for subsequent comparative analyses and decision-making processes.
This methodology ensures a robust analysis of NFT marketplaces by incorporating both onchain and offchain data, providing a holistic view of the ecosystem's dynamics and performance.

</div>

<div id="maintenance">

## Maintenance and Updates

Maintain the scraper by regularly updating the Python dependencies to mitigate security risks and ensure compatibility. Use pip to upgrade packages:

```bash
pip install --upgrade package-name
```

### Adding New DataProvider Abstract Methods

1. **Update DataProvider abstract base class**

   ```python
   from abc import ABC, abstractmethod

   class DataProvider(ABC):

       @abstractmethod
       def get_7day_volume(self):
           """Retrieve the volume of transactions over the past 7 days."""
           pass

       @abstractmethod
       def get_royalties_earned(self):
           """Calculate royalties earned from transactions."""
           pass

       @abstractmethod
       def get_example_data(self):
           """Retrieve some data"""
           pass

   ```

2. **Implementing Abstract Methods in Subclasses**

   ```python
   class NiftyProvider(DataProvider):

    def get_7day_volume(self):
        # Implementation specific to NiftyProvider
        pass

    def get_royalties_earned(self):
        # Implementation specific to NiftyProvider
        pass

    def get_some_data(self):
        # Some implementation
        return some_data_fetched

   ```

### Adding New Data Provider Subclass

1.  **Create a New DataProvider Subclass**

    To integrate a new marketplace to analyse, A new DataProvider has to be added. To create a DataProvider, create a subclass of the DataProvider abstract base class. This class must implement the required methods get_7day_volume and get_royalties_earned.

    Example Code:

    ```python
    from data_provider_base import DataProvider # Ensure the correct import path

    class NewMarketplaceProvider(DataProvider):

        @property
        def name(self) -> str:
            return "new_marketplace"

        def __init__(self):
            self._volume = None

        def get_7day_volume(self):
            # Implementation...
            return f"{self._volume:.2f}"

        def get_royalties_earned(self):
            # Implementation...
            return f"{royalties:.2f}"

    ```

2.  **Implement Data Fetching**  
    Fill in the fetch_volume_from_marketplace with logic specific to the new marketplace, whether it’s via API calls, web scraping, or another method.

3.  **Update the Configuration**  
    Add your new DataProvider to the list of providers in your main application module.

    ```python
    Example Code:
    data_providers = [
    NiftyProvider(),
    OpenseaProvider(),
    BlurProvider(),
    MagicEdenProvider(),
    NewMarketplaceProvider(), # Adding the new provider
    ]
    ```

</div>

<div id="License">

## License

Apache License 2.0

</div>
