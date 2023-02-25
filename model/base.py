from dictalchemy import DictableModel
from sqlalchemy.orm import declarative_base

Base = declarative_base(cls=DictableModel)
