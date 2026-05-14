import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

for year in range(2000, 2026):

    movies = pd.read_csv(f"movies_from_{year}.csv")
    movies['release_date'] = pd.to_datetime(movies['release_date'])
    movies['year'] = movies['release_date'].dt.year
    # try:
    #     movies['release_date'] = pd.to_datetime(movies['release_date'], format='mixed')

    # except Exception as e:
    #     print(f"Problem in {year}: {e}")
    #     break

    movies = movies[(movies['certification'] != 'NR') & (movies['vote_count'] > 500)]
    # movies = movies[(movies['vote_count'] > 500)]
    # movies = movies[(movies['certification'] != 'NR')]

    # sns.barplot(x=movies['year'], y=movies['vote_count'].mean())
    ax = sns.boxplot(data=movies, x='year', y='vote_count')
    ax.set_ylim([0, 12000])

    # sns.histplot(data=movies, x="certification")

    # sns.scatterplot(data=movies, x="budget", y="revenue")

    # sns.scatterplot(data=movies, x="runtime", y="revenue")
    
    # sns.scatterplot(data=movies, x="release_date", y="revenue")
    
    # sns.boxplot(data=movies, x='certification', y='revenue')
    # print(movies.describe())

    # sns.barplot(data=movies, x='release_date', y='vote_count')

    # sns.scatterplot(data=movies[movies['revenue'] > 1e7], x="revenue", y="vote_average")
    # sns.scatterplot(data=movies, x="budget", y="vote_average")

#     # print(movies.corr(numeric_only=True))

#     print(f'For {year}:')
#     print(f'Most expensive movie: {movies[movies['budget'] == movies['budget'].max()]['title']}, {movies[movies['budget'] == movies['budget'].max()]['budget']/1e6} mil $')
#     print(f'Most profitable movie: {movies[movies['revenue'] == movies['revenue'].max()]['title']}, {movies[movies['revenue'] == movies['revenue'].max()]['revenue']/1e6} mil $')
#     print(f'Top rated movie: {movies[movies['vote_average'] == movies['vote_average'].max()]['title']}, {movies[movies['vote_average'] == movies['vote_average'].max()]['vote_average']}/10')

# movies = pd.read_csv(f"movies_from_{2006}.csv")
# sns.displot(movies[movies['revenue'] > 1e6],x='revenue')

plt.show()