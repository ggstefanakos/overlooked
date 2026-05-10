import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

for year in range(2000, 2004):

    movies = pd.read_csv(f"movies_from_{year}.csv")
    # sns.histplot(data=movies[movies['certification'] != 'NR'], x="certification")

    sns.scatterplot(data=movies, x="budget", y="revenue")

    # sns.scatterplot(data=movies[movies['runtime']<200], x="runtime", y="revenue")
    # movies['release_date'] = pd.to_datetime(movies['release_date'], format='mixed')
    # sns.scatterplot(data=movies, x="release_date", y="revenue")
    # sns.scatterplot(data=movies[movies['revenue'] > 1e7], x="revenue", y="vote_average")
    # sns.scatterplot(data=movies, x="budget", y="vote_average")

#     # print(movies.corr(numeric_only=True))

#     print(f'For {year}:')
#     print(f'Most expensive movie: {movies[movies['budget'] == movies['budget'].max()]['title']}, {movies[movies['budget'] == movies['budget'].max()]['budget']/1e6} mil $')
#     print(f'Most profitable movie: {movies[movies['revenue'] == movies['revenue'].max()]['title']}, {movies[movies['revenue'] == movies['revenue'].max()]['revenue']/1e6} mil $')
#     print(f'Top rated movie: {movies[movies['vote_average'] == movies['vote_average'].max()]['title']}, {movies[movies['vote_average'] == movies['vote_average'].max()]['vote_average']}/10')

# movies = pd.read_csv(f"movies_from_{2003}.csv")
# sns.histplot(data=movies[movies['certification'] != 'NR'], x="certification")

plt.show()