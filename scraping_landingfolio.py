import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.landingfolio.com/inspiration/landing-page/business"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

rows = soup.find_all("div", class_="relative group text-center")

data_list = []

if rows:
    for row in rows:
        title = row.find("h3", class_="mt-4 text-base font-bold text-gray-900")
        date = row.find("p", class_="mt-1.5 text-xs font-medium text-gray-500")
        
    
        if title and date:
            data = {
                "title": title.text.strip(),
                "date": date.text.strip()
            }
            data_list.append(data)

json_file_path = 'data/landing_page_data_landingfolio.json' 
with open(json_file_path, 'w') as json_file:
    json.dump(data_list, json_file, indent=4)

print(f"Data telah disimpan ke {json_file_path}")
