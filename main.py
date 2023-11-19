import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ZILLOW_WEBSITE = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_SHEET = "https://forms.gle/L7tKAqzVhvYxMSPA9"

response = requests.get(ZILLOW_WEBSITE)
response.raise_for_status()
housing_website = response.text
soup = BeautifulSoup(housing_website, "html.parser")


scraped_price_list = [price.text.replace(',', '') for price in soup.find_all(name="div", class_="PropertyCardWrapper")]
numeric_rent_values = [int(re.search(r'\d+', value).group()) for value in scraped_price_list]
print(numeric_rent_values)

weblink_list = [weblink.get("href") for weblink in soup.find_all(class_="StyledPropertyCardDataArea-anchor")]
print(weblink_list)

address_list = [' '.join(address.text.split()).replace("\n", '').replace("|", '').strip() for address in soup.find_all(class_="StyledPropertyCardDataArea-anchor")]
print(address_list)