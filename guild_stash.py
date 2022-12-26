'''
Guild Stash Web Scraper

Author: Cearlmau

This simple program runs through a public guild stash and displays the unowned uniques.
Assuming cloudflare nor GGG changes their current setup as of 12/25/2022, this scraper should
be able to collect information about any public guild stash tab.
'''

import requests
import matplotlib as plot
import re
from bs4 import BeautifulSoup
import cloudscraper
import sys
from url import stash_info

scraper = cloudscraper.create_scraper()
base = "https://www.pathofexile.com/guild/view-stash/" + stash_info #Add relevant stash info here
map = {"Flask": 1, "Amulet":2, "Ring":3, "Claw":4, "Dagger":5, "Wand":6, "Sword":7, "Axe":8, "Mace":9, "Bow":10, "Staff":11, "Quiver":12, "Belt":13, "Gloves":14, "Boots":15, "Body Armour":16, "Helmet":17, "Shie;d":18, "Map":19, "Jewel":20, "Contract":22}

#This function searches through each section of the stash and provides information about each section
def scrape_all():

    sections = 22

    soup = BeautifulSoup(scraper.get(base).text, 'html.parser')
    stash_section_content = soup.find(class_="uniqueStash") #All of the unique stash
    total_progress = stash_section_content.find(class_="text") #Total progress of all uniques

    print("Missing Uniques: ")

    for i in range(sections):
        url = base + str(i + 1)
        url_stash_portion = url[27:]    
        page = scraper.get(url)


        if(page):
            soup = BeautifulSoup(page.text, 'html.parser')
            stash_section_content = soup.find(class_="uniqueStash")
            title = stash_section_content.find(href=re.compile(url_stash_portion))['title']
            portion_completion = stash_section_content.find(href=re.compile(url_stash_portion)).text
        
            items_unowned = soup.find_all(class_="item unowned")
            items_owned = soup.find_all(class_="item owned")
            if(len(items_unowned) != 0):
                print(title, str(round(len(items_unowned)/ (len(items_unowned) + len(items_owned)) * 100, 1)) + "%")

            item_unowned_set = []
            for item in items_unowned:
                item_unowned_set.append(item.find(class_="name").text)
            if(len(item_unowned_set) != 0):
                print(item_unowned_set)

            #js_info = soup.find_all("script")[3]
        '''
        f = open("test.txt", "w", encoding="utf-8")
        f.write(stash_section_content.prettify())
        f.close()
        '''

#This function searches through a specific portion of the stash
def scrape(number):
    url = base + str(number)
    page = scraper.get(url)
    url_stash_portion = url[27:]   

    soup = BeautifulSoup(page.text, 'html.parser')
    stash_section_content = soup.find(class_="uniqueStash")
    title = stash_section_content.find(href=re.compile(url_stash_portion))['title']
    portion_completion = stash_section_content.find(href=re.compile(url_stash_portion)).text

    items_unowned = soup.find_all(class_="item unowned")
    items_owned = soup.find_all(class_="item owned")
    if(len(items_unowned) != 0):
        print(title, str(round(len(items_unowned)/ (len(items_unowned) + len(items_owned)) * 100, 1)) + "%")

    item_unowned_set = []
    for item in items_unowned:
        item_unowned_set.append(item.find(class_="name").text)
    if(len(item_unowned_set) != 0):
        print(item_unowned_set)

#This function searches through the stash looking for all items matching the user input
def look_for(name):
    sections = 22
    status = 0
    item_set = set()
    for i in range(sections):
        url = base + str(i + 1)
        url_stash_portion = url[27:]    
        page = scraper.get(url)

        if(page):
            soup = BeautifulSoup(page.text, 'html.parser')
            stash_section_content = soup.find(class_="uniqueStash")
            title = stash_section_content.find(href=re.compile(url_stash_portion))['title']
            portion_completion = stash_section_content.find(href=re.compile(url_stash_portion)).text
        
            items_unowned = soup.find_all(class_="item unowned")
            items_owned = soup.find_all(class_="item owned")
            for item in items_owned:
                if name in removesyntax(item.find(class_="name").text):
                    item_set.add(title + ": " + item.find(class_="name").text + "(owned)")
                    status = 1
            for item in items_unowned:
                if name in removesyntax(item.find(class_="name").text):
                    item_set.add(title + ": " + item.find(class_="name").text + "(unowned)")
                    status = 1
    if status == 1:
        for item in item_set:
            print(item)
    else:
        print("No items found")

def removesyntax(word):
    return word.replace("'", "").replace("-","").lower().strip()
n = len(sys.argv)
print()
if(n == 1):
    scrape_all()
elif(n == 2):
    if(map.get(sys.argv[1].capitalize())):
        scrape(map[sys.argv[1].capitalize()])
    else:
        look_for(sys.argv[1].lower())
elif((sys.argv[1] + " " + sys.argv[2]).lower() == "body armour" 
        or (sys.argv[1] + " " + sys.argv[2]).lower() == "body armor"):
    scrape(map["Body Armour"])
elif(n > 10):
    print("Format: python guild_stash.py [item type/item name]")
else:
    name = ""
    for i in range(1, n):
        name = name + " " + sys.argv[i]
    print(name.strip())
    look_for(removesyntax(name))
print()