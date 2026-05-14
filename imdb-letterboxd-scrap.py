import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import pandas as pd

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
    text = soup.find('a', class_="averagerating tooltip")
    text = text['text']
    text_all = text.split()
    score = float(text_all[3])
    count = float(text_all[6].replace(','))
    return score, count

def get_imdb_score(soup):
    score = soup.find('span', class_='ipc-rating-star--rating')
    count = soup.find('span', class_='vote-count')
    
    if 'K' in count:
        count = float(count[:-1]) * 1e3
    elif 'M' in count:
        count = float(count[:-1]) * 1e6
    else:
        count = float(count)

    return float(score), count
    
def main():
    for year in range(2000, 2026):
        
        movies = pd.read_csv(f"movies_from_{year}.csv")
        
        for movie in movies: # nmz lathos thelei iloc isos?
            title = movie['title'].lower()
            title = title.replace(' ','-')

            letterboxd_url = f'https://letterboxd.com/film/{title}/'
            letterboxd_soup = make_soup(letterboxd_url)
            letterboxd_score, letterboxd_count = get_letterboxd_score(letterboxd_soup)

            movies['letterboxd_score'] = letterboxd_score
            movies['letterboxd_count'] = letterboxd_count

            imdb_url = f'https://www.imdb.com/title/{movie['imdb_id']}/'
            imdb_soup = make_soup(imdb_url)
            imdb_score, imdb_count = get_letterboxd_score(imdb_soup)

            movies['imdb_score'] = imdb_score
            movies['imdb_count'] = imdb_count

            movies.to_csv(f'movies_from_{year}.csv', index=False)



if __name__ == '__main__': main()