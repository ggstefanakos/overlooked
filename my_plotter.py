import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

movies = pd.read_csv("movies_from_2001.csv")

sns.scatterplot(data=movies, x="budget", y="revenue")
# sns.scatterplot(data=movies[movies['runtime']<200], x="runtime", y="revenue")
# movies['release_date'] = pd.to_datetime(movies['release_date'], format='mixed')
# sns.scatterplot(data=movies, x="release_date", y="revenue")
# sns.scatterplot(data=movies, x="revenue", y="vote_average")
# sns.scatterplot(data=movies, x="budget", y="vote_average")
print(movies.corr(numeric_only=True))
print(f'Most expensive movie: {movies[movies['budget'] == movies['budget'].max()]['title']}')
print(f'Most profitable movie: {movies[movies['revenue'] == movies['revenue'].max()]['title']}')

plt.show()