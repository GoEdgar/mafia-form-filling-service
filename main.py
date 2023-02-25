from bottle import run

from api.game.endpoint import app

if __name__ == '__main__':
    run(app)
