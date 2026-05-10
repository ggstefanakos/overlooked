import os
import pandas as pd
import tmdbsimple as tmdb
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import time

load_dotenv()
tmdb.API_KEY = os.getenv("MY_API_KEY")

def fetch_movie_data(movie_id):
    """Fetches details and certifications in a single request."""
    try:
        # append_to_response reduces network calls by 50%
        movie_obj = tmdb.Movies(movie_id)
        info = movie_obj.info(append_to_response='release_dates')
        
        # Extract certification logic
        certification = 'NR'
        results = info.get('release_dates', {}).get('results', [])
        for release in results:
            if release['iso_3166_1'] == 'US':
                for rd in release['release_dates']:
                    if rd['certification']:
                        certification = rd['certification']
                        break
        
        # Clean up unwanted keys efficiently
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
year = 2004
first_page = discover.movie(primary_release_year=year, page=1)
total_pages = first_page['total_pages']

all_movie_data = []

# Loop through pages (you can also parallelize this, but start here)
start = time.perf_counter()
# for page_num in range(1, min(total_pages, 5)): # Testing with 5 pages
for page_num in range(1, total_pages):
    tmp_time = time.perf_counter()
    print(f'Progress: {page_num*100/total_pages:6.3f} %  ({page_num:3d}/{total_pages}) ({int((tmp_time - start)//60):2d} min elapsed)',end='\r')
    response = discover.movie(primary_release_year=year, page=page_num)
    movie_ids = [m['id'] for m in response['results']]

    # Use ThreadPoolExecutor to fetch 10 movies at a time
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_movie_data, movie_ids))
    
    # Filter out None results from errors
    all_movie_data.extend([r for r in results if r])

# Create DataFrame once
df = pd.DataFrame(all_movie_data)
df.to_csv(f'movies_from_{year}.csv', index=False)
end = time.perf_counter()
print(f'Done with year {year} in {(end - start)//60} min')