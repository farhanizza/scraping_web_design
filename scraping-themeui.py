import requests
from bs4 import BeautifulSoup
import json
import os

json_file_path = 'data/landing_page_data_themeui.json' 

def load_existing_data(file_path):
    if os.path.exists(file_path):  
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return None

def save_data_if_changed(new_data, file_path):
    existing_data = load_existing_data(file_path)
    
    if existing_data != new_data:  
        with open(file_path, 'w') as json_file:
            json.dump(new_data, json_file, indent=4)
        print(f"Data has been saved to {file_path}")
    else:
        print(f"no changes from data, don't write a data {file_path}")


URL = "https://themeui.net/web-templates/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

page1 = soup.find_all("h2", class_="entry__title")

page2 = soup.find_all("div", class_="entry__excerpt")

data_list = []

data_list_new = []

if page1 and page2:
    for pages1, pages2 in zip(page1, page2):
        title = pages1.find("a").text.strip().replace(" \u2013 ", " ")
        title_cleaned = title.replace(" \u2014 ", " ")
        desc = pages2.find("p").text.strip()

        if title and desc:
            data = {
                "title": title_cleaned,
                "sneak_peek_desc": desc
            }
            data_list.append(data)
else:
    print("not found")

save_data_if_changed(data_list, json_file_path)

with open('data/landing_page_data_themeui.json', 'r') as file:
    data = json.load(file)

for v in data:
    URL_INTO = "https://themeui.net/" + v['title'].replace(" ", "-").lower()

    page_into = requests.get(URL_INTO)

    soup2 = BeautifulSoup(page_into.content, "html.parser")

    page3 = soup2.find("article", class_="content__primary freebie")

    if page3:
        description = page3.find("p")
        link = page3.find('a', class_='btn btn--primary')
        link_design = link.get('href')

        print()
        print(f"URL: {URL_INTO}")
        print(description.get_text(strip=True))
        print()
        print(f"Link Design: {link_design}")

        if description:
            data_description = {
                "title": v['title'],
                "sneak_peek_desc": v['sneak_peek_desc'],
                "description": description.get_text(strip=True),
                "link_design": link_design
            }
            data_list_new.append(data_description)
    else:
        print("not found")
        data_description = {
                "title": v['title'],
                "sneak_peek_desc": v['sneak_peek_desc'],
                "description": "not found"
        }
        data_list_new.append(data_description)

if os.path.exists(json_file_path):
    os.remove(json_file_path)
    print()
    print("File temporary has been deleted")
    print()
    with open(json_file_path, 'w') as json_file:
        json.dump(data_list_new, json_file, indent=4)
    print(f"Data has been saved tp {json_file_path}")
else:
    print("The File does not exist")

