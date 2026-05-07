import tmdbsimple as tmdb
import os
from dotenv import load_dotenv

load_dotenv()

tmdb.API_KEY = os.getenv("MY_API_KEY")

# response = tmdb.Movies(100).info()
# print(response["title"])
discover = tmdb.Discover()
response = discover.movie(release_date_gte="2000-01-01", release_date_lte="2000-12-31")

results = response["results"]
for result in results:
    print(f'{result["release_date"]}\t{result["title"]}')