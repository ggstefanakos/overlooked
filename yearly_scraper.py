import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()

tmdb.API_KEY = os.getenv("MY_API_KEY")

discover = tmdb.Discover()
years = [x for x in range(2000, 2010, 1)]

start = time.perf_counter()

total_pages = 2
i = 1
movie = tmdb.Movies(25508).info()
movie.pop('belongs_to_collection')
movie.pop('genres')
movie.pop('origin_country')
movie.pop('production_companies')
movie.pop('production_countries')
movie.pop('spoken_languages')

releases = tmdb.Movies(25508).release_dates()['results']
for release in releases:
    if release['iso_3166_1'] == 'US':
        movie['certification'] = 'NR'
        for j in release['release_dates']:
            if j['certification'] != '' and j['certification'] != 'NR':
                movie['certification'] = j['certification']
            
df = pd.DataFrame(movie, index=[0])

while i < total_pages:
    response = discover.movie(primary_release_year=years[0], page=i)
    total_pages = response["total_pages"]
    tmp_time = time.perf_counter()
    print(f'Progress: {i*100/total_pages:.3f} %  ({i:3d}/{total_pages}) ({int((tmp_time - start)//60):2d} min elapsed)')
    results = response["results"]

    for result in results:
        movie = tmdb.Movies(result['id']).info()
        movie.pop('belongs_to_collection')
        movie.pop('genres')
        movie.pop('origin_country')
        movie.pop('production_companies')
        movie.pop('production_countries')
        movie.pop('spoken_languages')

        releases = tmdb.Movies(result['id']).release_dates()['results']
        for release in releases:
            if release['iso_3166_1'] == 'US':
                movie['certification'] = 'NR'
                for j in release['release_dates']:
                    if j['certification'] != '' and j['certification'] != 'NR':
                        movie['certification'] = j['certification']

        df.loc[len(df)] = movie
    i += 1
    # if i == 3: break

df = df.drop(0)
df.to_csv(f'movies_from_{years[0]}.csv',index=False)

end = time.perf_counter()
print(f'Done with year {years[0]} in {(end - start)//60} min')