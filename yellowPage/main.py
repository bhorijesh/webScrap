import requests
import pandas as pd
from bs4 import BeautifulSoup

Business = []
url = "https://www.yellowpagesnepal.com/agricultural-equipment-and-implements"

while True:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    listing = soup.find_all('h3', class_="font-20 t400")
    for i in listing:
        business_name = i.get_text(strip=True)  
        business_link = i.find('a')['href']  
        business_link = "https://www.yellowpagesnepal.com/" + business_link
        Business.append([business_name, business_link])
       
    next_page = soup.find('a', string="Next")
    if next_page:
        url = "https://www.yellowpagesnepal.com/" + next_page['href']
    else:
        break

ad = pd.DataFrame(Business , columns=['BusinesName','Businesslink'])
ad.to_csv("sal.csv")

print("Done") 