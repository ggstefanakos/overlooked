import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def make_soup(url): # Returns BeautifulSoup Object of the url's page
    sleep(1)
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def save_page(url, filename): # Save the html of a page locally
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"}
    r = requests.get(url, headers=headers)
    with open(filename,'wb') as f:
        f.write(r.content)

def load_page(filename): # Load locally saved html
    with open(filename, 'rb') as f:
        return f.read()
    
def get_letterboxd_score(soup):
    page = soup.select("script")
    for element in page:
        if '{"image":' in str(element):
            desired_element = str(element)

    desired_element = desired_element.split(',')
    for value in desired_element:
        if 'ratingValue' in value:
            score = value.split(':')
            score = float(score[1])
        if 'ratingCount' in value:
            count = value.split(':')
            count = float(count[1])

    return score, count

# def get_letterboxd_page_soup(title):
#     title = title.lower()
#     title = title.replace(' ','-')
    
#     title_page_soup = make_soup(url=f'https://letterboxd.com/film/{title}/')

#     if 'Letterboxd - Not Found' not in title_page_soup.find('title'):
#         return title_page_soup
#     else:
#         search_page_url = f'https://letterboxd.com/search/{title}/'

#         title_page_soup = search_page_url + '1st result'
#         return title_page_soup

def get_letterboxd_page(imdb_id):
    url = f'https://letterboxd.com/search/films/imdb:{imdb_id}/'

    page_url = '1st result' + url

    return page_url

def get_imdb_score(url):
    service = Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)

    driver.get(url)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ipc-rating-star--rating"))
    )
    imdb_score = float(driver.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "vote-count"))
    )

    imdb_count = driver.find_element(By.CLASS_NAME, "vote-count").text

    sleep(0.5)

    driver.quit()

    if 'K' in imdb_count:
        imdb_count = float(imdb_count[:-1]) * 1e3
    elif 'M' in imdb_count:
        imdb_count = float(imdb_count[:-1]) * 1e6
    else:
        imdb_count = float(imdb_count)

    return imdb_score, imdb_count
    
def main():
    # id = 157336 #interstellar
    save_page('https://letterboxd.com/imdb/tt0816692','int.html')
    
    # for year in range(2000, 2026):
    year = 2003    
    movies = pd.read_csv(f"movies_from_{year}.csv")
    all_letterboxd_score = []
    all_letterboxd_count = []
    all_imdb_score = []
    all_imdb_count = []

    # for imdb_id in movies['imdb_id']:
        # letterboxd_page = get_letterboxd_page(imdb_id)

        # letterboxd_score, letterboxd_count = get_letterboxd_score(letterboxd_page)
        # all_letterboxd_score.append(letterboxd_score)
        # all_letterboxd_count.append(letterboxd_count)

        # imdb_url = f'https://www.imdb.com/title/{imdb_id}/'
        # imdb_score, imdb_count = get_imdb_score(imdb_url)
        # all_imdb_score.append(imdb_score)
        # all_imdb_count.append(imdb_count)
        # print(f'[{imdb_id}] Score: {imdb_score}, count: {imdb_count}')

    # movies['letterboxd_score'] = all_letterboxd_score
    # movies['letterboxd_count'] = all_letterboxd_count

    # movies['imdb_score'] = all_imdb_score
    # movies['imdb_count'] = all_imdb_count

    # movies.to_csv(f'more_from_movies_from_{year}.csv', index=False)

if __name__ == '__main__': main()