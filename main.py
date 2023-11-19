import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ZILLOW_WEBSITE = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORMS = "https://forms.gle/L7tKAqzVhvYxMSPA9"

response = requests.get(ZILLOW_WEBSITE)
response.raise_for_status()
housing_website = response.text
soup = BeautifulSoup(housing_website, "html.parser")

#create lists with price, address and link data
scraped_price_list = [price.text.replace(',', '') for price in soup.find_all(name="div", class_="PropertyCardWrapper")]
numeric_rent_values = [int(re.search(r'\d+', value).group()) for value in scraped_price_list]
print(numeric_rent_values)

address_list = [' '.join(address.text.split()).replace("\n", '').replace("|", '').strip() for address in soup.find_all(class_="StyledPropertyCardDataArea-anchor")]
print(address_list)

weblink_list = [weblink.get("href") for weblink in soup.find_all(class_="StyledPropertyCardDataArea-anchor")]
print(weblink_list)

# Keep Chrome browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORMS)
sleep(1)

#fill in forms by looping over the lists created from Zillow
for n in range(len(numeric_rent_values)):

    address_filing = driver.find_element(By.CSS_SELECTOR, 'input.whsOnd.zHQkBf[jsname="YPqjbf"][aria-labelledby="i1"]')
    address_filing.send_keys(address_list[n])
    address_filing.send_keys(Keys.TAB)

    price_filing = driver.find_element(By.CSS_SELECTOR, 'input.whsOnd.zHQkBf[jsname="YPqjbf"][aria-labelledby="i5"]')
    price_filing.send_keys(numeric_rent_values[n])
    price_filing.send_keys(Keys.TAB)

    weblink_filing = driver.find_element(By.CSS_SELECTOR, 'input.whsOnd.zHQkBf[jsname="YPqjbf"][aria-labelledby="i9"]')
    weblink_filing.send_keys(weblink_list[n])
    weblink_filing.send_keys(Keys.TAB)

    button = driver.find_element(By.CSS_SELECTOR, 'span.NPEfkd.RveJvd.snByac')
    button.click()

    return_main_page = driver.find_element(By.PARTIAL_LINK_TEXT, 'Nog een antwoord')
    return_main_page.click()
    sleep(1)S

driver.quit()
print(f'all data is added')
