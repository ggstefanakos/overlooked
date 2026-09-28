import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

movies = pd.read_csv(f"movies_from_{2000}.csv")

for year in range(2001, 2026):
    movies = pd.concat([movies.copy(), pd.read_csv(f"movies_from_{year}.csv")])

    # movies['release_date'] = pd.to_datetime(movies['release_date'])
    # movies['year'] = movies['release_date'].dt.year
    # try:
    #     movies['release_date'] = pd.to_datetime(movies['release_date'], format='mixed')

    # except Exception as e:
    #     print(f"Problem in {year}: {e}")
    #     break

    # sns.barplot(x=movies['year'], y=movies['vote_count'].mean())
    # ax = sns.boxplot(data=movies, x='year', y='vote_count')
    # ax.set_ylim([0, 12000])

    # sns.scatterplot(data=movies, x="runtime", y="revenue")
    
    # sns.scatterplot(data=movies, x="release_date", y="revenue")

    # sns.scatterplot(data=movies, x="budget", y="vote_average")

    # print(f'For {year}:')
    # print(f'Most expensive movie: {movies[movies['budget'] == movies['budget'].max()]['title']}, {movies[movies['budget'] == movies['budget'].max()]['budget']/1e6} mil $')
    # print(f'Most profitable movie: {movies[movies['revenue'] == movies['revenue'].max()]['title']}, {movies[movies['revenue'] == movies['revenue'].max()]['revenue']/1e6} mil $')
    # print(f'Top rated movie: {movies[movies['vote_average'] == movies['vote_average'].max()]['title']}, {movies[movies['vote_average'] == movies['vote_average'].max()]['vote_average']}/10')


movies = movies[(movies['certification'] != 'NR') & (movies['vote_count'] > 500) & (movies['budget'] < 3.3e8) & (movies['budget'] > 10e6)]
# movies = movies[(movies['budget'] < 50e6)] #Low budget filtering
movies['release_date'] = pd.to_datetime(movies['release_date'])
movies['year'] = movies['release_date'].dt.year

# print(movies.corr(numeric_only=True))
# print(f'{movies['certification'].value_counts()}')

sns.lmplot(data=movies, x="budget", y="revenue", hue='certification', scatter=True, height=15)
# plt.savefig(f"budget_revenue_line_plot.png", bbox_inches='tight')
plt.show()