import random
import sqlalchemy
import string
import sys
#from django.contrib.auth import hashers
#from django.conf import settings
import pandas as pd
from tqdm import tqdm

# Load existing table into dataframe
db_url = sys.argv[1]
engine = sqlalchemy.create_engine(db_url)
conn = engine.connect()
users = pd.read_sql(
    'SELECT id, name FROM users',
    engine
)

total, = conn.execute(
    sqlalchemy.sql.text('SELECT count(*) from users')
).fetchone()
pbar = tqdm(total=total)

# Add password hashes

#settings.configure(DEBUG=True)
pw_len = 8
char_pool = string.ascii_letters + string.digits

for i, user in enumerate(users.itertuples()):
    username = user.name.replace(' ', '').lower()
    pw = ''.join(
        random.choice(char_pool)
        for _ in range(pw_len)
    )
    #pw_hash = hashers.make_password(pw)
    while True:
        try:
            conn.execute(
                sqlalchemy.sql.text(
                    'UPDATE users '
                    'SET password = :pw, username = :username '
                    'WHERE id = :user_id'
                ),
                username=username,
                pw=pw,
                user_id=user.id
            )
        except sqlalchemy.exc.IntegrityError:
            username += random.choice(string.digits)
            continue
        break
    pbar.update(1)

conn.close()
