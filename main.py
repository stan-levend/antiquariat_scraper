import requests
import re
import csv
from bs4 import BeautifulSoup


def antikvart(query):
  url = f"https://www.antikvart.sk/site/Vyhladavanie.html?sv={query.strip().lower().replace(' ','+')}"
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')
  print(query.upper())

  print('ANTIKVART \nPAGE 1 \n')
  search_antikvart_page(soup)
  print('\n')

  element = soup.find('div', class_='mr_vypis_line_2')
  n_books = int(element.strong.get_text())

  #find if query request got less than 10 books, if yes, continue to another author
  if n_books <= 10:
    # print('______________________')
    return
  else:
    n_pages = n_books // 10
    for i in range(2, n_pages + 2):
      url = f"https://www.antikvart.sk/site/Vyhladavanie.html?sv={query.strip().lower().replace(' ','+')}&page={i}"
      req = requests.get(url)
      soup = BeautifulSoup(req.content, 'html.parser')
      print(f'PAGE {i}\n')
      search_antikvart_page(soup)
      
def search_antikvart_page(soup):
  for book in soup.find_all("div", class_="tc_popis"):
    print(book.h3.a.get_text())
    print(book.find('strong').get_text())
    print(book.h2.a.get_text(), '\n')

def antiqart(query):
  url = f"https://www.antiqart.sk/search/node/{query.strip().lower().replace(' ','%20')}"
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')
  
  print('ANTIQART \nPAGE 1\n')
  search_antiqart_page(soup)

  #find if query request got more than 1 page, if not, continue to another author
  pages = soup.find('li', class_='pager-last')
  if(pages is None): 
    print('______________________')
    return
  else:
    n_pages = re.findall(r'\d+', pages.a.get('href'))[-1] #regex to find number (int) of pages 
    #browse through every page
    for i in range(1, int(n_pages) + 1):
      url = f"https://www.antiqart.sk/search/node/{query.strip().lower().replace(' ','%20')}?page={i}"
      req = requests.get(url)
      soup = BeautifulSoup(req.content, 'html.parser')
      print(f'PAGE {i+1}\n')
      search_antiqart_page(soup)
      
    print('______________________')

def search_antiqart_page(soup):
  for book in soup.find_all("li", class_="search-result"):
    search = book.div.p.get_text()
    if 'Stav skladu:' in search:
      print(book.h3.a.get_text())
      print(search.strip(), '\n')

if __name__ == "__main__":
  queries = [
  # 'chesterton', 'nesbo', 'chiang', 'tolkien', 'rovelli', 'tolstoj',
  # 'lewis', 'dostojevski', 'orwell', 'eldredge', 'tegmark', 'peterson', 'doyle', 'asimov', 'feynman', 'eriksen', ''
  # 'rovelli', 'smolin', 'hawking', 'tyson', 'eriksen', 'wheeler archibald'
  ]

  with open('queries.txt', 'r') as fd:
      reader = csv.reader(fd)
      for row in reader:
        if row[0][0] == '#':
          continue
        # print(row)
        queries.extend(row)
  
  for query in queries:
    antikvart(query)
    antiqart(query)
    # pass