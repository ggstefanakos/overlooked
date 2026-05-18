import requests
from bs4 import BeautifulSoup
from time import sleep, perf_counter
import pandas as pd
from random import uniform
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Each thread gets its own persistent IMDB driver
thread_local = threading.local()

N_THREADS = 4  # Tune this — too high and you'll get banned


def make_driver():
    service = Service(executable_path="geckodriver.exe")
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(service=service, options=options)


def get_imdb_driver():
    """Return this thread's persistent IMDB driver, creating it if needed."""
    if not hasattr(thread_local, 'imdb_driver'):
        thread_local.imdb_driver = make_driver()
    return thread_local.imdb_driver


def make_soup(url):
    sleep(0.5)
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')


def get_letterboxd_score(soup):
    page = soup.select("script")
    for element in page:
        if '{"image":' in str(element):
            desired_element = str(element)

    desired_element = desired_element.split(',')
    for value in desired_element:
        if 'ratingValue' in value:
            lb_score = float(value.split(':')[1])
        if 'ratingCount' in value:
            lb_count = float(value.split(':')[1])

    return lb_score, lb_count


def get_letterboxd_page(imdb_id, driver):
    driver.get(f"https://letterboxd.com/imdb/{imdb_id}")
    return driver.current_url


def get_imdb_score(imdb_id, driver):
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


def scrape_movie(row):
    """Scrape one movie. Runs inside a thread."""
    i, movie = row
    imdb_id = movie['imdb_id']
    sleep(uniform(0.1, 0.5))

    # Use this thread's persistent IMDB driver
    imdb_driver = get_imdb_driver()
    imdb_score, imdb_count = get_imdb_score(imdb_id, imdb_driver)

    # Fresh driver for Letterboxd every time (avoids bot detection)
    lb_driver = make_driver()
    try:
        letterboxd_url = get_letterboxd_page(imdb_id, lb_driver)
    finally:
        lb_driver.quit()

    letterboxd_score, letterboxd_count = get_letterboxd_score(make_soup(letterboxd_url))

    return i, imdb_score, imdb_count, letterboxd_score, letterboxd_count


def main():
    for year in range(2000, 2026):
        start = perf_counter()
        print(f'Year {year}:')
        movies = pd.read_csv(f"movies_from_{year}.csv")
        results = {}

        with ThreadPoolExecutor(max_workers=N_THREADS) as executor:
            futures = {
                executor.submit(scrape_movie, row): row[0]
                for row in movies.iterrows()
            }

            completed = 0
            for future in as_completed(futures):
                try:
                    i, imdb_score, imdb_count, lb_score, lb_count = future.result()
                    results[i] = (imdb_score, imdb_count, lb_score, lb_count)
                except Exception as e:
                    i = futures[future]
                    print(f'\tError on row {i}: {e}')
                    results[i] = (None, None, None, None)

                completed += 1
                elapsed = perf_counter() - start
                print(f'\tProgress: {completed/len(movies):.2%} ({completed}/{len(movies)}) | Elapsed: {elapsed/60:.2f} min',end='\r')

        # Reassemble in original order
        movies['imdb_score']       = [results[i][0] for i in range(len(movies))]
        movies['imdb_count']       = [results[i][1] for i in range(len(movies))]
        movies['letterboxd_score'] = [results[i][2] for i in range(len(movies))]
        movies['letterboxd_count'] = [results[i][3] for i in range(len(movies))]

        movies.to_csv(f'more_from_movies_from_{year}.csv', index=False)

    # Clean up all thread-local IMDB drivers
    if hasattr(thread_local, 'imdb_driver'):
        thread_local.imdb_driver.quit()


if __name__ == '__main__':
    main()