import requests
import re
import csv
from bs4 import BeautifulSoup


def antikvart(query):
  url = f'https://www.antikvart.sk/site/Vyhladavanie.html?sv={query.strip().lower().replace(" ","+")}'
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')
  print('QUERY:', query)

  print('------------------ANTIKVART------------------\nPAGE 1\n')
  search_antikvart_page(soup)

  element = soup.find('div', class_='mr_vypis_line_2')
  n_books = int(element.strong.get_text())

  #find if query request got less than 10 books, if yes, continue to another author
  if n_books <= 10:
    return

  n_pages = n_books // 10
  for i in range(2, n_pages + 2):
    url = f'https://www.antikvart.sk/site/Vyhladavanie.html?sv={query.strip().lower().replace(" ","+")}&page={i}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'PAGE {i}\n')
    search_antikvart_page(soup)

def search_antikvart_page(soup):
  for book in soup.find_all('div', class_='tc_popis'):
    title_tag = book.h2.a
    print(title_tag.get_text())

    author_tag = book.h3.a
    print(author_tag.get_text())

    publisher = book.text.splitlines()[3].strip()
    print(publisher)

    price = book.find('strong')
    print(price.get_text(), '\n')



def paseka(query):
  url = f'http://www.paseka.sk/index.php?&s_text={query.strip().lower().replace(" ","%20")}&order=timeof&page=katalog'
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')

  print('------------------PASEKA------------------\nPAGE 1\n')
  search_paseka_page(soup)

  #find if query request got more than 1 page, if not, continue to another author
  pages_tag = soup.find('p', class_='pages')
  if pages_tag is None or pages_tag.get_text() == 'Neboli nájdené žiadne knihy.':
    return
  else:
    n_pages = int(re.findall(r'\d+', pages_tag.get_text())[1])
    #browse through every page
    for i in range(2, n_pages + 1):
      url = f'http://www.paseka.sk/index.php?&s_text={query.strip().lower().replace(" ","%20")}&pg={i}&order=timeof&page=katalog'
      req = requests.get(url)
      soup = BeautifulSoup(req.content, 'html.parser')
      print(f'PAGE {i}\n')
      search_paseka_page(soup)


def search_paseka_page(soup):
  for book in soup.find_all('div', class_='book-data'):
    title_tag = book.h3.a
    print(title_tag.get_text())

    parent_tag = book.div
    author_tag = parent_tag.a
    print(author_tag.get_text())

    publisher_year_tag = parent_tag.find('span', class_='data')
    print(publisher_year_tag.get_text())

    price_tag = parent_tag.div.a.span
    print(price_tag.get_text(), '\n')




def antiqart(query):
  url = f'https://www.antiqart.sk/search/node/{query.strip().lower().replace(" ","%20")}'
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')

  print('------------------ANTIQART------------------\nPAGE 1')
  search_antiqart_page(soup, url)

  #find if query request got more than 1 page, if not, continue to another author
  pages_tag = soup.find('li', class_='pager-last')
  if pages_tag is None:
    print('__________________________________________________________________________________')
    return

  n_pages = int(re.findall(r'\d+', pages_tag.a.get('href'))[-1]) #regex to find number (int) of pages

  #browse through every page
  for i in range(1, n_pages + 1):
    url = f'https://www.antiqart.sk/search/node/{query.strip().lower().replace(" ","%20")}?page={i}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'PAGE {i+1}')
    search_antiqart_page(soup, url)
  print('__________________________________________________________________________________')


def search_antiqart_page(soup, url):
  for book in soup.find_all('li', class_='search-result'):
    parent_tag = book.div.p.get_text()
    if 'Stav skladu:' in parent_tag:
      # title_tag = book.h3.a
      # print(title_tag.get_text())

      # contents = parent_tag.split()
      # start_index = contents.index('tovaru:') + 2
      # end_index= contents.index('Dostupné')
      # author_string = ' '.join(contents[start_index:end_index])
      # print(author_string)

      url = book.h3.a['href']
      req = requests.get(url)
      concrete_soup = BeautifulSoup(req.content, 'html.parser')

      title_tag = concrete_soup.find('div', class_='field field-name-title field-type-ds field-label-hidden').div.h1
      print(title_tag.get_text())

      author_tag = concrete_soup.find('div', class_='field field-name-field-book-author field-type-taxonomy-term-reference field-label-hidden').div.div.a
      print(author_tag.get_text())

      publisher_tag = concrete_soup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden').find('div', class_='field-item even').findChildren('p')
      print(publisher_tag[-1].get_text())

      price_tag = concrete_soup.find('span', class_='uc-price')
      print(price_tag.get_text(), '\n')




def antikvariatshop(query):
  url = f'https://www.antikvariatshop.sk/vyhledavani/?all={query.strip().lower().replace(" ","+")}'
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')

  print('------------------ANTIKVARIATSHOP------------------\nPAGE 1\n')
  search_antikvariatshop_page(soup)

  pages_tag = soup.find('p', class_='zobrazeno')
  books_per_page = 36
  total_books_string = pages_tag.strong.get_text()
  total_books = int(re.findall(r'\d+', total_books_string)[0])

  if total_books == 0:
    return

  n_pages = total_books // books_per_page
  if total_books % books_per_page != 0:
    n_pages += 1

  if n_pages == 0:
    return

  #browse through every page
  for i in range(2, n_pages + 1):
    url = f'https://www.antikvariatshop.sk/vyhledavani/strana-{i}/?all={query.strip().lower().replace(" ","+")}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'PAGE {i}\n')
    search_antikvariatshop_page(soup)


def search_antikvariatshop_page(soup):
  data = soup.find('table', class_='katalog').find('tbody')
  for book in data.find_all('tr'):

    title_tag = book.td
    print(title_tag.get_text())

    author_tag = title_tag.find_next_sibling()
    print(author_tag.get_text())

    condition_tag = author_tag.find_next_sibling()
    print('Condition:', condition_tag.img['alt'])

    price_tag = condition_tag.find_next_sibling()
    print(price_tag.get_text(), '\n')



if __name__ == '__main__':
  queries = [
  # 'jules verne'
  # 'doyle'
  # 'chesterton', 'nesbo', 'chiang', 'tolkien', 'rovelli', 'tolstoj',
  # 'lewis', 'dostojevski', 'orwell', 'eldredge', 'tegmark', 'peterson', 'doyle', 'asimov', 'feynman', 'eriksen', ''
  # 'rovelli', 'smolin', 'hawking', 'tyson', 'eriksen', 'wheeler archibald'
  ]

  # input = input()
  # queries.append(str(input))

  with open('queries.txt', 'r') as fd:
      reader = csv.reader(fd)
      for row in reader:
        if row[0][0] == '#':
          continue
        # print(row)
        queries.extend(row)

  for query in queries:
    antikvart(query)
    paseka(query)
    antikvariatshop(query)
    antiqart(query)