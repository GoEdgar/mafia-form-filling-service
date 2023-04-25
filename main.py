from bottle import run

from api.app import app
from api.game import endpoint
from api.day import endpoint

if __name__ == '__main__':
    run(app)
