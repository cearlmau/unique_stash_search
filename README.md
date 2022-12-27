# Unique Stash Search
Searches through a public guild stash on pathofexile.com. This is mainly used to check for unique completion in a league where a guild is 
looking to acquire all the uniques in the game.

The web scraper works off the assumption that you have a defined url which allows you to access a public unique guild stash. From then on, it scrapes each section of the website, and depending on which function you call retrieves the appropriate portions of unique items. Request/Cloudscraper and BeautifulSoup are utilized to acquire and parse through the retrieved data, respectively.

In addition to the two executable python files(`guild_stash.py` and `pathofguilding.py`) you also need to create an additional file (`url.py`) or edit `guild_stash.py` to include the `stash_info` portion of the url needed for the HTTPS request.

`guild_stash.py` is a standalone terminal-based program that (may) require additional user input via line arguments. `pathofguilding.py` requires `guild_stash.py`, and users can change the input and view the output in an external window GUI. Both are functionally identical with minor variations in presentation of data.
