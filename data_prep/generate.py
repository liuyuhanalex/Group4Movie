import faker
import itertools as it
import numpy as np
import os
import pandas as pd
import sqlalchemy
import sys

db_url = sys.argv[1]
data_path = sys.argv[2]
num_users = int(sys.argv[3])
engine = sqlalchemy.create_engine(db_url)

rating_totals_raw = pd.read_csv(
    os.path.join(data_path, 'ratings.tsv'),
    dtype={'averageRating': np.float_, 'numVotes': np.int_},
    sep='\t'
).set_index('tconst')

titles = pd.read_sql(
    'SELECT id, imdb_id FROM titles',
    engine,
    index_col='imdb_id'
)

rating_totals = (
    rating_totals_raw.join(titles, how='inner')
    [['id', 'averageRating', 'numVotes']]
)

total_votes = rating_totals['numVotes'].sum()
user_ids = range(num_users)

rates_titles = []
rates_ratings = []

for _, row in rating_totals.iterrows():
    id_, avg, votes = row
    n = round(votes / 100)

    # Include at least one vote for titles with any votes
    if votes > 0:
        n = max(1, n)

    rates_titles.extend(it.repeat(id_, n))
    rates_ratings.extend(
        (
            max(1, min(10, round(x)))
            for x in np.random.normal(loc=avg, size=n)
        )
    )

rates = pd.DataFrame(
    list(zip(
        it.islice(it.cycle(user_ids), 0, int(total_votes)),
        rates_titles,
        rates_ratings
    )),
    columns=['user_id', 'title_id', 'rating']
)

print(rates)

fake = faker.Faker()
users = pd.DataFrame(
    ((i, fake.name()) for i in user_ids),
    columns=['id', 'name']
)

users.to_sql('users', engine, if_exists='append', index=False)
rates.to_sql('rates', engine, if_exists='append', index=False)
