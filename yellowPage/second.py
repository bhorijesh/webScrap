import pandas as pd
import requests
from bs4 import BeautifulSoup

address = []
last_updated = []
categories = []
description = []
phone = []
email = []
url = 'https://www.yellowpagesnepal.com/agricultural-equipment-and-implements'

def extract_info(soup):
    addresses = soup.find_all('span', itemprop="streetAddress")
    descriptions = soup.find_all('div', class_="details info-row")
    last_updated = soup.find_all ('div', class_ = "updated-date float-lef")
    return [a.get_text(strip=True) for a in addresses], [d.get_text(strip=True) for d in descriptions]

def extract_business_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    addresses, descriptions  = extract_info(soup)
    for addr, desc, in zip(addresses, descriptions,):
        address.append(addr)
        last_updated.append("lu")  
        categories.append("")  
        description.append(desc)
        phone.append("")  
        email.append("")  

    next_page = soup.find('a', string="Next")
    if next_page:
        url = "https://www.yellowpagesnepal.com/" + next_page['href']
        extract_business_info(url)

extract_business_info(url)

ad =pd.read_csv('sal.csv')

for x in ad['Businesslink']:
    r = requests.get(x)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract "Last Updated" info
    updated_date = soup.find('div', class_="updated-date float-left")
    if updated_date:
        last_updated.append(updated_date.get_text(strip=True))
    else:
        last_updated.append(None)

    # Extract phone and email
    info = soup.find('div', class_="contact-content")
    
    # Extract phone
    if info is not None:
        ph = info.find('p')
        if ph is not None:
            phone_img = ph.find_all('img')[-1]['src'] if ph.find_all('img') else None
            if phone_img:
                phone_number = phone_img.split('=')[1]  # Assuming phone number is split by '='
                phone.append(phone_number)
            else:
                phone.append(None)
        else:
            phone.append(None)
    else:
        phone.append(None)

    # Extract email
    email_meta = info.find('meta', {'itemprop': "email"}) if info else None
    if email_meta:
        email.append(email_meta['content'])  # Assuming email is in content attribute
    else:
        email.append(None)

df = pd.DataFrame({
    'Address': address,
    'Last Updated': last_updated,   
    'Categories': categories,
    'Description': description,
    'Phone': phone,
    'Email': email,
})
df.to_csv('3.csv')

print("Done")