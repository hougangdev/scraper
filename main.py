import httpx
from selectolax.parser import HTMLParser

# url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"
url = "https://opensea.io/rankings?sortBy=seven_day_volume"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

resp = httpx.get(url, headers=headers)
html = HTMLParser(resp.text) # Parse the HTML content

containers = html.css('span[data-id="TextBody"]')

for container in containers:
    print(container.text(deep=True))
print(containers)