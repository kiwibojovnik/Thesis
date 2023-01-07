import fileinput
import os
import requests
from bs4 import BeautifulSoup
import io


MAX_ARTICLES_ON_PAGE = 15

def get_articles(root_url, number_of_pages):
    """Function printing python version."""
    page = 0
    links = ""

    while page != number_of_pages:
        url = "{}{}".format(root_url, page)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        for anchor in soup.find_all('section', {"class": "articles-list"}):
            for a in anchor.find_all('a', href=True):
                links += a['href']+'\n'
        page = page + 1

    return links


#Do I need this function? 
def save_articles(links, filename):
    """Function for saving the file."""
    f = open(filename, "a", encoding="utf8")
    f.write(links)
    f.close()

#Get the number of page
def get_number_of_pages(root_url):
    """"Function for geetting exact page numbers of the web page"""

    r = requests.get(root_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    number = "0"
    for anchor in soup.find('div', {"class": "pagination"}):
        x = anchor.text.isnumeric()
        if x:
            number = anchor.text

    return number

def append_article_to_file(str, filename):
    """Function for append the new links on the web page to file with links"""
    with open(filename,'r', encoding="utf8") as f:
        with open('newfile.txt','w', encoding="utf8") as f2: 
            f2.write(str)
            f2.write(f.read())
    os.remove(filename)
    os.rename('newfile.txt',filename)


def get_new_articles(root_url, number_of_pages, filename):
    """Function for getting only the new articles."""

    expected_number_of_pages = 2

    breaker = False
    while expected_number_of_pages <= number_of_pages:

        actual_links = get_articles(root_url, expected_number_of_pages)
        saved_links = open(filename, "r", encoding="utf8")

        #Get fisrt line – link from file with saved links to article
        first_line = saved_links.readline()

        new_articles = ""
        count = 0

        for line_actual in io.StringIO(actual_links):
            if first_line == line_actual:
                breaker = True
            else:
                count = count + 1
                if count > MAX_ARTICLES_ON_PAGE :
                    expected_number_of_pages = expected_number_of_pages + 1
                    count = 0

            new_articles += line_actual

        if breaker:
            break

    append_article_to_file(new_articles, filename)


def get_all_articles(root_url, filename):
    """Function printing all articles from root url."""
    page = 1
    links = ""

    saved_links = open("articles"+{root_url}+".txt", "a", encoding="utf8")

    article = ""
    for line in saved_links:
        url = "{}{}".format(root_url, line)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')


        #for anchor in soup.find_all('article', {"class", "detail"}):
        #    print(anchor.text)
        #    return


ROOT_URL_OF_PAGE = "https://www.parlamentnilisty.cz/archiv?p="
NUMBER_OF_PAGES = 20 #get_number_of_pages(ROOT_URL_OF_PAGE)


get_new_articles(ROOT_URL_OF_PAGE, int(NUMBER_OF_PAGES), "hajaja.txt")
#get_all_articles(ROOT_URL_OF_PAGE, "hajaja.txt")
