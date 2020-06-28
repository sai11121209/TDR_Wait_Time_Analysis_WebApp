import pandas as pd
from os import path
from sqlalchemy import create_engine

path = path.join(path.dirname(__file__), "sampledata20200218.csv")
df = pd.read_csv(path, encoding="utf_8")[0:9900]
print(type(df))
engine = create_engine(
    "postgres://dhabazyzjfedir:2e4c78147c903a92957d41ccd261a37f384dcfb7277845ca6f7e13982b089229@ec2-35-172-73-125.compute-1.amazonaws.com:5432/d8nkht2bie0dah"
)
df.to_sql("standbytime_standbytimedata", con=engine, if_exists="append", index=False)

