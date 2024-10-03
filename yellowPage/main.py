import requests
import pandas as pd
from bs4 import BeautifulSoup

Business = []
url = "https://www.yellowpagesnepal.com/agricultural-equipment-and-implements"

while True:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Finding all the listings on the page
    lis = soup.find_all('div', id="nav-home")
    for listing in lis:
        business_names = listing.find_all('h3', class_="font-20 t400")
        for i in business_names:
            business_name = i.get_text(strip=True)
            business_link = i.find('a')['href']
            business_link = "https://www.yellowpagesnepal.com/" + business_link
            Business.append([business_name, business_link])
    
    # Find the next page link
    next_page = soup.find('a', string="Next")
    if next_page:
        url = "https://www.yellowpagesnepal.com/" + next_page['href']
    else:
        break

# Saving the data into a CSV file
ad = pd.DataFrame(Business, columns=['BusinessName', 'BusinessLink'])
ad.to_csv("sal.csv", index=False)

print("Done")
