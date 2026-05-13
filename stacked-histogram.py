import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates

movies = pd.concat([pd.read_csv(f"movies_from_{year}.csv") for year in range(2000,2010)])
movies = movies.reset_index(drop=True)

movies['release_date'] = pd.to_datetime(movies['release_date'])
movies['year'] = movies['release_date'].dt.year
movies['norm_date'] = movies['release_date'].apply(lambda x: x.replace(year=1996))
# movies['day_of_year'] = movies['release_date'].dt.dayofyear

# filtering
movies = movies[(movies['certification'] != 'NR') & (movies['vote_count'] > 500)]

plt.figure()
ax = sns.histplot(data=movies, x='norm_date',multiple='stack', hue='year', bins=52)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.show()