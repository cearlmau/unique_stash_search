from guild_stash import BeautifulSoup, scraper, base, sections, re, map, removesyntax

# Gets all sections of unique stash. Returns in following format (string, dict), where string is
# total completion fraction, and dict is each section, where key is section title and value is
# (owned list, unowned list) 
def get_all():
    soup = BeautifulSoup(scraper.get(base).text, 'html.parser')
    stash_section_content = soup.find(class_="uniqueStash") #All of the unique stash
    total_progress = stash_section_content.find(class_="text") #Total progress of all uniques
    
    all = {}
    for i in range(sections):
        url = base + str(i + 1)
        url_stash_portion = url[27:]    
        page = scraper.get(url)

        if(page):
            soup = BeautifulSoup(page.text, 'html.parser')
            stash_section_content = soup.find(class_="uniqueStash")
            title = stash_section_content.find(href=re.compile(url_stash_portion))['title']
        
            items_unowned = soup.find_all(class_="item unowned")
            items_owned = soup.find_all(class_="item owned")
            item_unowned_set = []
            item_owned_set = []
            for item in items_unowned:
                item_unowned_set.append(item.find(class_="name").text)
            for item in items_owned:
                item_owned_set.append(item.find(class_="name").text)
            all[title] = (item_owned_set, item_unowned_set)
    return (total_progress.text, all)
            
            
# Gets a section of the unique stash tab based on argument
# Returns in following format: dict, where key is the title of the section
# and value is (owned list, unowned list)
def get_section(title):
    if map.get(title.capitalize()):
        url = base + str(map[title.capitalize()])
        page = scraper.get(url)
        url_stash_portion = url[27:]   

        soup = BeautifulSoup(page.text, 'html.parser')
        stash_section_content = soup.find(class_="uniqueStash")
        title = stash_section_content.find(href=re.compile(url_stash_portion))['title']
    
        items_unowned = soup.find_all(class_="item unowned")
        items_owned = soup.find_all(class_="item owned")
        item_unowned_set = []
        item_owned_set = []
        for item in items_unowned:
            item_unowned_set.append(item.find(class_="name").text)
        for item in items_owned:
            item_owned_set.append(item.find(class_="name").text)
        return {title:(item_owned_set, item_unowned_set)}
    return ()
        

def search(name):
    item_set = []
    for i in range(sections):
        url = base + str(i + 1)
        url_stash_portion = url[27:]    
        page = scraper.get(url)

        if(page):
            soup = BeautifulSoup(page.text, 'html.parser')
            stash_section_content = soup.find(class_="uniqueStash")
            title = stash_section_content.find(href=re.compile(url_stash_portion))['title']

            items_unowned = soup.find_all(class_="item unowned")
            items_owned = soup.find_all(class_="item owned")
            for item in items_owned:
                if name in removesyntax(item.find(class_="name").text):
                    item_set.append((item.find(class_="name").text, title, "owned"))
            for item in items_unowned:
                if name in removesyntax(item.find(class_="name").text):
                    item_set.append((item.find(class_="name").text, title, "unowned"))
    return item_set


if __name__ == "__main__":
    t = search("black")
    print(t)