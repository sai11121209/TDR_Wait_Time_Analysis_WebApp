import pandas as pd
from os import path
from sqlalchemy import create_engine

pathtdl = path.join(path.dirname(__file__), "sampledata20200218_tdl.csv")
pathtds = path.join(path.dirname(__file__), "sampledata20200218_tds.csv")
dftdl = pd.read_csv(pathtdl, encoding="utf_8")[0:4500]
dftds = pd.read_csv(pathtds, encoding="utf_8")[0:4500]
engine = create_engine(
    "postgres://dhabazyzjfedir:2e4c78147c903a92957d41ccd261a37f384dcfb7277845ca6f7e13982b089229@ec2-35-172-73-125.compute-1.amazonaws.com:5432/d8nkht2bie0dah"
)
dftdl.to_sql(
    "standbytime_standbytimedatatdl", con=engine, if_exists="append", index=False
)
dftdl.to_sql(
    "standbytime_standbytimedatatds", con=engine, if_exists="append", index=False
)

