import pandas as pd
import sqlalchemy
import csv
import numpy as np
from pandas.io import sql
import sys
import os
import logging


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.ERROR)

    db_url = sys.argv[1]
    data_path = sys.argv[2]
    conn = sqlalchemy.create_engine(db_url)

    print('Finish connect with MySQL!')

    table_files = [
        ('title_types', 'title_types.csv'),
        ('titles', 'titles.csv'),
        ('genres', 'genres.csv'),
        ('has_genre', 'has_genres.csv'),
        ('episodes', 'episodes.csv'),
        ('people', 'people.csv'),
        ('known_for', 'known_for.csv'),
        ('writes', 'writes.csv'),
        ('directs', 'directs.csv'),
        ('professions', 'professions.csv'),
        ('has_profession', 'has_professions.csv'),
    ]

    for table, file_ in table_files:
        df = pd.read_csv(
            os.path.join(data_path, file_),
            sep='\t',
            low_memory=False
        )
        src_len = len(df)
        dst_len, = sql.execute(f'SELECT count(*) from {table}', conn).fetchone()
        if src_len != dst_len:
            sql.execute(f'DELETE FROM {table}', conn)
            df.to_sql(
                name=table,
                con=conn,
                if_exists='append',
                chunksize=100000,
                index=False,
            )
        print(f'{table} is finished!')

    print('Finished All!')
