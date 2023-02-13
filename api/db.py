from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dictalchemy import DictableModel

Base = declarative_base(cls=DictableModel)

# TODO: credentials from envs
engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres", echo=True)

Session = sessionmaker(engine)