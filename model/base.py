from dictalchemy import DictableModel
from sqlalchemy.orm import declarative_base


class CustomBase(DictableModel):
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


Base = declarative_base(cls=CustomBase)
