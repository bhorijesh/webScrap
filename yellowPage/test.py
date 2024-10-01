import pandas as pd
import requests
from bs4 import BeautifulSoup

address = []
last_updated = []
Categories = []
description = []
phone = []
email = []
url = 'https://www.yellowpagesnepal.com/agricultural-equipment-and-implements'

def extract_info(soup):
    addresses = soup.find_all('span', itemprop="streetAddress")
    descriptions = soup.find_all('div', class_="details info-row")
    return [a.get_text(strip=True) for a in addresses], [d.get_text(strip=True) for d in descriptions]

def extract_business_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    addresses, descriptions  = extract_info(soup)
    for addr, desc, in zip(addresses, descriptions,):
        address.append(addr)
        description.append(desc)
          
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
                phone_number = phone_img.split('=')[1]  # phone number is split by '='
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
        email.append(email_meta['content'])  # email is in content attribute
    else:
        email.append(None)
        
    # Extract categories
    cat = soup.find('div', class_="description mb-5 pt-3")
    if cat:
        for cate in cat.find('a'):
            if cate is not None:
                Categories.append(cate.get_text(strip=True))
    else:
        Categories.append(None)



# Ensure all lists are of the same length
max_length = max(len(address), len(last_updated), len(Categories), len(description), len(phone), len(email))

# Padding lists to ensure they have the same length
address += [None] * (max_length - len(address))
last_updated += [None] * (max_length - len(last_updated))
Categories += [None] * (max_length - len(Categories))
description += [None] * (max_length - len(description))
phone += [None] * (max_length - len(phone))
email += [None] * (max_length - len(email))

# Now create the DataFrame
df = pd.DataFrame({
    'Address': address,
    'Last Updated': last_updated,
    'Categories': Categories,
    'Description': description,
    'Phone': phone,
    'Email': email,
})

final_df = pd.concat([ad, df], axis=1)

final_df.to_csv('final.csv',index=False)

print("Done")