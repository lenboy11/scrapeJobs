from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import csv

accentureWeb = 'https://www.accenture.com/'
PATH = "C:\Program Files (x86)\chromedriver.exe"
source = requests.get( accentureWeb + 'de-de/careers/jobsearch?' ).text

soup = BeautifulSoup(source, 'lxml')

countrylist = soup.find('ul', class_="countrylist")
links = []
for country in countrylist.find_all(class_='list-group-item'):
    link = country['data-country-site']
    if 'en' in link or 'de' in link:
        links.append( country['data-country-site'] )

driver = webdriver.Chrome(PATH)
for link in links:
    driver.get(accentureWeb + link + "/careers/jobsearch?jk=trainee")

    # search = driver.find_element_by_id('job-search-hero-bar')
    # search.send_keys("trainee")
    # search.send_keys(Keys.RETURN)

    time.sleep(1)


driver.get('https://www.accenture.com/api/sitecore/JobSearch/FindJobs')
print(driver)


driver.quit()



print('#country-language-selector')
