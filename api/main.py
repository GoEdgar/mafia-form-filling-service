from bottle import run
from sqlalchemy import create_engine

from api.app import app
from api.day.endpoint import *
from api.game.endpoint import *
from models import Base

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
Base.metadata.create_all(engine)
run(app)