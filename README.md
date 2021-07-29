# Antiquart book scraper

This scraper uses <code>BeautifulSoup</code> and <code>requests</code>  to scrape data from multiple antiqart book shops located in Kosice, Slovakia. The output will list the query results that consist of the query in form of an author of book (book title) and price for the book.

Currently added sites to scrape:
* [Antikvart](https://www.antikvart.sk/)
* [Antiqart](https://www.antiqart.sk/)
* [Paseka](http://www.paseka.sk/index.php?)
### How To Use

At the terminal, type:
```
python3 main.py
```
which will execute the main script that read queries from <code>queries.txt</code>.

### <code>queries.txt</code>  example input:
```
chesterton, nesbo, chiang, tolkien
# tolstoj, lewis
#dostojevski, orwell
```
will only add first line to the list of queries.
Use `#` at the start of the line to exclude the line from the list of queries.

## Things to add in the future:
- Add other sites to scrape.
    - [x] http://www.paseka.sk/index.php?
    - [ ] https://www.wallstreet.sk/antique.php
    - [ ] https://www.pokladyzpovaly.sk/
    - [ ] https://www.usialenca.sk/
    - [ ] https://www.antikvariatshop.sk/
    - [ ] https://www.antikvariatik.sk/?

- [ ] Divide shops into separate `.py` files
- [ ] Add delivery options and prices.
- [x] Add txt file for queries input.
- [ ] Take input directly from command line.
- [ ] Make GUI.