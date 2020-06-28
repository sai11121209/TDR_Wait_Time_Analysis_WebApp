import pandas as pd
from os import path
from sqlalchemy import create_engine

path = path.join(path.dirname(__file__), "sampledata20200218.csv")
df = pd.read_csv(path)

engine = create_engine(
    "postgres://stiarglydckmrw:d726c958201e561102606b1dc3ce840dc7aa3b1c1eb04d7e283b59c965e17796@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d22lnkqidjha62"
)
df.DataFrame.to_sql(
    standbytime_standbytimedata, con=engine, if_exists="append", index=False
)

