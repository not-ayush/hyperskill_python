""""
-----------------
STAGE 1
-----------------
import requests
url = input("Input the URL:")
r = requests.get(url)
r_json = r.json()
if r.status_code != 200 or 'content' not in r_json:
    print("Invalid quite resource!")
else:
    print(r_json["content"])
-----------------
STAGE 2
----------------
import requests
from bs4 import BeautifulSoup

url = input()
# check if link is correct or not
if not ('articles' in url and 'nature.com' in url):
    print('Invalid page!')
else:
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    info = dict.fromkeys(['title', 'description'])
    title = soup.find('title').text
    desc = soup.select("meta[name='description']")[0].get('content')
    info['title'] = title
    info['description'] = desc
    print(info)

-----------------
STAGE 3
----------------

import requests

source = open("source.html", "wb")
r = requests.get(input("Input the URL:"))

if r:
    source.write(r.content)
    print("Content saved.")
else:
    print(f"The URL returned {r.status_code}!")

-----------------
STAGE 4
----------------
import requests
from bs4 import BeautifulSoup
import string
r = requests.get("https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3")
soup_list_page = BeautifulSoup(r.content, 'html.parser')

'''
basically save the text from all the news type articles
and the title should not have whitespace (use underscore) or punctuation (remove)

made a mistake, the url passed is a page that has links to different articles,
first we gotta find the ones to do the following stuff on
----
so there is one div (say A) that has two divs, one is meta, other contains link to article
we need to get a list of all type A, loop through them, then use the h2 + p selector to get all the
divs that contain the meta for the former after a bit of looking at the page
I found there's items on each page, so a for loop range(20) will work and can
compare and add only the news ones to a new list
'''



def save_file(url):
    article_page = requests.get(url)
    soup = BeautifulSoup(article_page.content, 'html.parser')
    # get title and article texts
    title_raw = soup.find('h1').text
    article = soup.select('.article__teaser')[0].text
    # add the correct characters for title to a list then store it as string when done
    title_lst = []
    for i in title_raw:
        if i in string.punctuation:
            pass
        elif i in string.whitespace:
            title_lst.append('_')
        else:
            title_lst.append(i)
    title = ''.join(title_lst)
    # save the content in file
    with open(f'{title}.txt', 'w', encoding='utf-8') as file:
        file.write(article)


# on the article lists page get the article types and links
article_type = soup_list_page.select('.c-meta__type')
article_links = soup_list_page.select('.c-card__link')
news_article_urls = []

# add the article links to a new list which have type as "News"
for j in range(20):  # len(soup_list_page.find_all('app-article-list-row__item'))
    if article_type[j].text == "News":
        news_article_urls.append(article_links[j].get('href'))

# loop through the News urls and save to file
for x in news_article_urls:
    save_file(f"https://www.nature.com{x}")
"""
import requests
from bs4 import BeautifulSoup
import string
import os
'''
alright so, here we gotta do the thing we did on one page but on multiple pages, 
and the user says what category and how many pages they want starting from page 1,
and the file must be saved in proper directory like: Page_N/%article_title%.txt
CSS SELECTOR FOR NEXT LINK:  
li.c-pagination__item[data-page="next"] > a.c-pagination__link 
SO THE PROPER ALGO:
ask user for no of pages and category
loop through each page and do the save file thing:
    the directory for all pages must be created even if no files are there

WHAT IT DOES:
save the articles from this catalog https://www.nature.com/nature/articles?sort=PubDate&year=2020 on this link
according to the number of pages the user specified, and according to the category user specified.
The articles are saved in proper directories according to pages, and the titles of the files are proper
'''

no_of_pages = int(input("Enter no of pages: "))
type_of_article = input("Enter article type: ")
# https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=2


def save_file(url, n):
    article_page = requests.get(url)
    soup = BeautifulSoup(article_page.content, 'html.parser')
    # get title and article texts
    title_raw = soup.find('h1').text
    article = soup.select('.article__teaser')[0].text
    # add the correct characters for title to a list then store it as string when done
    title_lst = []
    for i in title_raw:
        if i in string.punctuation:
            pass
        elif i in string.whitespace:
            title_lst.append('_')
        else:
            title_lst.append(i)
    title = ''.join(title_lst)
    # save the content in file f'Page_{n}\\{title}.txt'
    os.mkdir(f'Page_{n}')
    with open(os.path.join(f'Page_{n}', f'{title}.txt'), 'w', encoding='utf-8') as file:
        file.write(article)


for page_n in range(1, no_of_pages+1):
    r = requests.get("https://www.nature.com/nature/articles?sort=PubDate&year=2020" if page_n == 1 else
                     f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page_n}")
    soup_list_page = BeautifulSoup(r.content, 'html.parser')
    # on the article lists page get the article types and links
    article_type = soup_list_page.select('.c-meta__type')
    article_links = soup_list_page.select('.c-card__link')
    news_article_urls = []

    # add the article links to a new list which have type as "News"
    for j in range(20):  # len(soup_list_page.find_all('app-article-list-row__item'))
        if article_type[j].text == type_of_article:
            news_article_urls.append(article_links[j].get('href'))

    # loop through the News urls and save to file or if no articles found just create directory
    if len(news_article_urls) != 0:
        for x in news_article_urls:
            save_file(f"https://www.nature.com{x}", page_n)
    else:
        os.mkdir(f"Page_{page_n}")
