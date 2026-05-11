import os
import pandas as pd
import tmdbsimple as tmdb
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import time

load_dotenv()
tmdb.API_KEY = os.getenv("MY_API_KEY")

# Define keys to drop outside the function for a tiny speed boost
EXCLUDE_KEYS = {'belongs_to_collection', 'genres', 'origin_country', 
                'production_companies', 'production_countries', 
                'spoken_languages', 'release_dates'}

def fetch_movie_data(movie_id):
    try:
        movie_obj = tmdb.Movies(movie_id)
        info = movie_obj.info(append_to_response='release_dates')
        
        # Faster certification extraction
        certification = 'NR'
        for release in info.get('release_dates', {}).get('results', []):
            if release.get('iso_3166_1') == 'US':
                for rd in release.get('release_dates', []):
                    if rd.get('certification'):
                        certification = rd['certification']
                        break
                break # Found US, no need to check other countries
        
        # Efficient filtering
        filtered_data = {k: v for k, v in info.items() if k not in EXCLUDE_KEYS}
        filtered_data['certification'] = certification
        return filtered_data
    except Exception:
        return None

# --- Main Logic ---
discover = tmdb.Discover()
years = range(2005, 2025)

# 1. Keep the executor open for the entire process
with ThreadPoolExecutor(max_workers=15) as executor:
    for year in years:
        start = time.perf_counter()
        
        # Get first page to find total count
        first_page = discover.movie(primary_release_year=year, page=1)
        total_pages = first_page['total_pages']
        
        all_movie_data = []

        if total_pages <= 500:
            for page_num in range(1, min(501, total_pages + 1)):
                # Fetch the list of IDs for the current page
                try:
                    response = discover.movie(primary_release_year=year, page=page_num)
                    movie_ids = [m['id'] for m in response.get('results', [])]
                    
                    # 2. Map the work to the existing thread pool
                    results = list(executor.map(fetch_movie_data, movie_ids))
                    all_movie_data.extend([r for r in results if r])

                    # if page_num % 10 == 0:
                    elapsed = (time.perf_counter() - start) / 60
                    print(f'Year {year} | Progress: {page_num/total_pages:>5.1%} ({page_num}/{total_pages}) | Elapsed: {elapsed:3.1f} min',end='\r')
                
                except Exception as e:
                    print(f"Error on page {page_num}: {e}")
                    continue
        else:
            for page_num in range(1, total_pages + 1):
                # Fetch the list of IDs for the current page
                try:
                    response = discover.movie(primary_release_year=year, page=page_num) # na to kano ana eksamiino
                    movie_ids = [m['id'] for m in response.get('results', [])]
                    
                    # 2. Map the work to the existing thread pool
                    results = list(executor.map(fetch_movie_data, movie_ids))
                    all_movie_data.extend([r for r in results if r])

                    # if page_num % 10 == 0:
                    elapsed = (time.perf_counter() - start) / 60
                    print(f'Year {year} | Progress: {page_num/total_pages:>5.1%} ({page_num}/{total_pages}) | Elapsed: {elapsed:3.1f} min',end='\r')
                
                except Exception as e:
                    print(f"Error on page {page_num}: {e}")
                    continue

        # Save year-end data
        if all_movie_data:
            df = pd.DataFrame(all_movie_data)
            df.to_csv(f'movies_from_{year}.csv', index=False)
            
        print(f'Completed {year} in {(time.perf_counter() - start)/60:.2f} min')