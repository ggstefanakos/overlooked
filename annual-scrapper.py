import os
import pandas as pd
import tmdbsimple as tmdb
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import time
from calendar import monthrange

load_dotenv()
tmdb.API_KEY = os.getenv("MY_API_KEY")

def fetch_movie_data(movie_id):
    """Fetches details and certifications in a single request."""
    try:
        movie_obj = tmdb.Movies(movie_id)
        info = movie_obj.info(append_to_response='release_dates')
        
        # Extract certification logic
        certification = 'NR'
        results = info.get('release_dates', {}).get('results', [])
        for release in results:
            if release['iso_3166_1'] == 'US':
                for rd in release['release_dates']:
                    if rd['certification'] and rd['certification'] != 'NR':
                        certification = rd['certification']
                        break
        
        # Clean up unwanted keys
        exclude = {'belongs_to_collection', 'genres', 'origin_country', 
                   'production_companies', 'production_countries', 'spoken_languages', 'release_dates'}
        filtered_data = {k: v for k, v in info.items() if k not in exclude}
        filtered_data['certification'] = certification
        
        return filtered_data
    except Exception as e:
        print(f"Error fetching ID {movie_id}: {e}")
        return None

# --- Main Logic ---
discover = tmdb.Discover()
years = range(2015, 2026)
month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
for year in years:
    start = time.perf_counter()
    last_time = 0.0

    all_movie_data = []
    print(f'Year {year}:')
    for month in range(1,13):
        print(f'\n\t{month_names[month]}:')
        _, last_day = monthrange(year, month)

        first_page = discover.movie(primary_release_date_gte=f'{year}-{month}-01',primary_release_date_lte=f'{year}-{month}-{last_day}', page=1)
        total_pages = first_page['total_pages']

        for page_num in range(1, total_pages + 1):

            print(f'\t\tProgress: {page_num/total_pages:.2%} ({page_num}/{total_pages}) | Elapsed: {(time.perf_counter() - start)/60:.2f} min (+{(time.perf_counter() - start - last_time)/60:.2f} min)',end='\r')
            response = discover.movie(primary_release_date_gte=f'{year}-{month}-01',primary_release_date_lte=f'{year}-{month}-{last_day}', page=page_num)
            movie_ids = [m['id'] for m in response['results']]

            # Use ThreadPoolExecutor to fetch 10 movies at a time
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(fetch_movie_data, movie_ids))

            # Filter out None results from errors
            all_movie_data.extend([r for r in results if r])

        last_time = time.perf_counter()

    # Create DataFrame once
    df = pd.DataFrame(all_movie_data)
    df.to_csv(f'movies_from_{year}.csv', index=False)
    print(f'\nDone with year {year}.')