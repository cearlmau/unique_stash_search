'''
Guild Stash Web Scraper

Author: Cearlmau

This simple program runs through a public guild stash and displays the unowned uniques.
Assuming cloudflare nor GGG changes their current setup as of 12/25/2022, this scraper should
be able to collect information about any public guild stash tab and display it in GUI window.
'''

from guild_stash import BeautifulSoup, scraper, base, sections, re, map, removesyntax

import tkinter as tk
from tkinter import ttk

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
        
# Gets all uniques matching the input name
# return a list of matching uniques in the format of
# (item name, item type title, owned/unowned)
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
                if removesyntax(name) in removesyntax(item.find(class_="name").text):
                    item_set.append((item.find(class_="name").text, title, "owned"))
            for item in items_unowned:
                if removesyntax(name) in removesyntax(item.find(class_="name").text):
                    item_set.append((item.find(class_="name").text, title, "unowned"))
        
    return item_set


# Helper function to format total progress
# Returns a list of 2 numbers
def total_progress(number):
    return [int(i) for i in number.split("/")]

# Handles all gui related display
def display(t, a):
    
    #init details
    root = tk.Tk()
    root.geometry('450x450')
    root.title('Path of Guilding')
    root.grid()

    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)

    t = total_progress(t)


    # label
    l = tk.Label(root, text = "Total Unique Item Collection Progress")
    l.config(font =("Courier", 12))

    #progress bar
    style = ttk.Style(root)
    style.layout('text.Horizontal.TProgressbar', 
                [('Horizontal.Progressbar.trough',
                {'children': [('Horizontal.Progressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'}), 
                ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
    percentage = round((t[0]/t[1]) * 100)
    style.configure('text.Horizontal.TProgressbar', text= str(percentage) + ' %', anchor='center')
    variable = tk.DoubleVar(root)
    pbar = ttk.Progressbar(root, style='text.Horizontal.TProgressbar', variable=variable, length=350)
    pbar.step(percentage)

    #navigation
    var = tk.StringVar(root)
    var.set("All Uniques")
    def OptionMenu_Select(e):
        listbox.delete(0, tk.END)
        a = {}
        if var.get() == "All Uniques":
            t, a = get_all()
        else:
            a = get_section(var.get())
        list_insert(listbox, a)

    list = map.keys()
    dropdown = tk.OptionMenu(root, var,"All Uniques", *list, command=OptionMenu_Select)

    # list
    listbox = tk.Listbox(root, height = 10,width = 25,bg = "grey",
            activestyle = 'dotbox',font = "Helvetica",fg = "white",)  
    list_insert(listbox, a)
    # searchbar
    search_frame = tk.Frame(root, )
    text = tk.Text(search_frame, width=30, height=1)
    text.insert('1.0','''''')
    def search_button_select():
        listbox.delete(0, tk.END)
        a = search(text.get("1.0",'end-1c'))
        text.delete("1.0", "end")
        for i, t, s in a:
            listbox.insert("1", i + ": " + s)
    def search_button_select2(e):
        listbox.delete(0, tk.END)
        a = search(text.get("1.0",'end-2c'))
        text.delete("1.0", "end")
        for i, t, s in a:
            listbox.insert("1", i + ": " + s)
    search_button = tk.Button(search_frame, text="search", command=search_button_select)


    l.pack()
    pbar.pack()
    dropdown.pack()
    listbox.pack(fill="both", expand=True)
    search_frame.pack()
    text.pack(side=tk.LEFT)
    search_button.pack(side=tk.LEFT)

    root.bind('<Return>', search_button_select2)
    root.mainloop()


def list_insert(listbox, a):
    for section in a:
        for i, unowned in enumerate(a[section]):
            if i == 1:
                for item in unowned:
                    listbox.insert("1", item)



if __name__ == "__main__":
    t, a = get_all()
    display(t, a)




