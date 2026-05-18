import requests
from bs4 import BeautifulSoup
from time import sleep, perf_counter
import pandas as pd
from random import uniform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def make_soup(url): # Returns BeautifulSoup Object of the url's page
    sleep(0.5)
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
    
def get_letterboxd_score(soup): # Returns the letterboxd star rating (out of 5) and the number of ratings
    page = soup.select("script")
    for element in page:
        if '{"image":' in str(element):
            desired_element = str(element)

    desired_element = desired_element.split(',')
    for value in desired_element:
        if 'ratingValue' in value:
            score = float(value.split(':')[1])
        if 'ratingCount' in value:
            count = float(value.split(':')[1])

    return score, count

def get_letterboxd_page(imdb_id, driver): # Returns the letterboxd url that corresponds to the specific imdb_id

    driver.get(f"https://letterboxd.com/imdb/{imdb_id}")    
    page_url = driver.current_url

    return page_url

def get_imdb_score(imdb_id, driver): # Returns the imdb star rating (out of 10) and the number of ratings

    driver.get(f'https://www.imdb.com/title/{imdb_id}/')

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ipc-rating-star--rating"))
    )
    imdb_score = float(driver.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "vote-count"))
    )

    imdb_count = driver.find_element(By.CLASS_NAME, "vote-count").text

    if 'K' in imdb_count:
        imdb_count = float(imdb_count[:-1]) * 1e3
    elif 'M' in imdb_count:
        imdb_count = float(imdb_count[:-1]) * 1e6
    else:
        imdb_count = float(imdb_count)

    return imdb_score, imdb_count

def make_driver():
    service = Service(executable_path="geckodriver.exe")
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(service=service, options=options)
    # return webdriver.Firefox(service=service)
    
def main():
    
    for year in range(2000, 2026):
        start = perf_counter()
        print(f'Year {year}:')
        movies = pd.read_csv(f"movies_from_{year}.csv")
        all_letterboxd_score = []
        all_letterboxd_count = []
        all_imdb_score = []
        all_imdb_count = []

        for i, movie in movies.iterrows():
            imdb_id = movie['imdb_id']

            driver = make_driver()

            print(f'\tProgress: {(i+1)/(len(movies)):.2%} ({i+1}/{len(movies)}) | Elapsed: {(perf_counter() - start)/60:.2f} min',end='\r')

            imdb_score, imdb_count = get_imdb_score(imdb_id, driver)
            all_imdb_score.append(imdb_score)
            all_imdb_count.append(imdb_count)

            letterboxd_page = get_letterboxd_page(imdb_id, driver)
            driver.quit()

            letterboxd_score, letterboxd_count = get_letterboxd_score(make_soup(letterboxd_page))
            all_letterboxd_score.append(letterboxd_score)
            all_letterboxd_count.append(letterboxd_count)

            sleep(uniform(1,2))

        movies['letterboxd_score'] = all_letterboxd_score
        movies['letterboxd_count'] = all_letterboxd_count

        movies['imdb_score'] = all_imdb_score
        movies['imdb_count'] = all_imdb_count

        movies.to_csv(f'more_from_movies_from_{year}.csv', index=False)

if __name__ == '__main__': main()