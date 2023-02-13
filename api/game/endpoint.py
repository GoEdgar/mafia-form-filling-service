import json

from bottle import request, response
from pydantic import ValidationError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from api.app import app
from api.db import Session
from models import GameModel, DayModel
from .validation import GameCreateRequest, GamePatchRequest, GameResponse


@app.post("/game")
def create_game():
    try:
        game_data = GameCreateRequest(**request.json)
    except ValidationError as e:
        response.status = 400
        return {"error": str(e)}

    with Session() as session:
        new_game = GameModel(**game_data.dict(exclude={"days"}))
        new_game.days = [DayModel(**day.dict(exclude_none=True)) for day in game_data.days]
        session.add(new_game)

        try:
            session.commit()
        except IntegrityError:
            response.status = 409
            return {
                "error": "The day with specified number already exists in the game"
                }

        response.content_type = "application/json"
        return GameResponse.from_orm(new_game).json()


@app.get("/game")
def get_all_games():
    with Session() as session:
        games = session.query(GameModel).all()

        response.content_type = "application/json"
        return json.dumps([json.loads(GameResponse.from_orm(game).json()) for game in games])


@app.get("/game/<game_id>")
def get_game(game_id: int):
    with Session() as session:
        game = session.query(GameModel).filter(GameModel.id == game_id).one_or_none()

        if game is None:
            response.status = 404
            return {"error": "Game not found"}

        response.content_type = "application/json"
        return GameResponse.from_orm(game).json()


@app.route("/game/<game_id>", "PATCH")
def update_game(game_id: int):
    try:
        game_data = GamePatchRequest(**request.json)
    except ValidationError as e:
        return {"error": str(e)}

    with Session() as session:
        is_game_present = session.query(GameModel).where(
            GameModel.id == game_id).update(game_data.dict())
        if not is_game_present:
            response.status = 404
            return {"error": "Game not found"}

        session.commit()


@app.delete("/game/<game_id>")
def delete_game(game_id: int):
    with Session() as session:
        game = session.query(GameModel).where(GameModel.id == game_id).one_or_none()
        if game is None:
            response.status = 404
            return {"error": "Game not found"}

        session.delete(game)
        session.commit()