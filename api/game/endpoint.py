from datetime import datetime

import orjson
from bottle import request, response, Bottle
from pydantic import ValidationError
from pydantic.json import pydantic_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from api.db import Session
from api.models import GameModel, DayModel
from .validation import GameCreateRequest, GamePatchRequest, GameResponse

app = Bottle()


@app.post('/game')
def create_game():
    try:
        game_data = GameCreateRequest(**request.json)
    except ValidationError as e:
        response.status = 400
        return {'error': str(e)}

    with Session() as session:
        new_game = GameModel(**game_data.dict(exclude={'days'}))
        new_game.inserted_at = datetime.now()
        new_game.days = [DayModel(**day.dict(exclude_none=True)) for day in
                         game_data.days]
        session.add(new_game)

        try:
            session.commit()
        except IntegrityError:
            response.status = 409
            return {
                'error':
                    'The day with specified number already exists in the game.'
            }

        response.content_type = 'application/json'
        return GameResponse.from_orm(new_game).json(by_alias=True)


@app.get('/game')
def get_all_games():
    with Session() as session:
        # get the limit and page parameters from the request
        limit = int(request.query.get('limit', 10))
        page = int(request.query.get('page', 1))
        if limit < 1 or page < 1:
            response.status = 400
            return {
                'error': '"page" and "limit" params must be greater than 0.'}

        # calculate the offset based on the limit and page number
        offset = (page - 1) * limit

        # Query a subset of games based on the given limit and offset,
        # and eagerly load the 'days' relationship
        # using joinedload to avoid the N+1 problem
        # when accessing the 'days' attribute of each GameModel instance
        games = session.query(GameModel) \
            .limit(limit) \
            .offset(offset) \
            .options(joinedload(GameModel.days))

        # return the subset of games as a JSON response
        response.content_type = 'application/json'
        return orjson.dumps(
            tuple(GameResponse.from_orm(game) for game in games),
            default=pydantic_encoder
        )


@app.get('/game/<game_id>')
def get_game(game_id: int):
    with Session() as session:
        game = session.query(GameModel).filter(
            GameModel.id == game_id).one_or_none()

        if game is None:
            response.status = 404
            return {'error': 'Game not found'}

        response.content_type = 'application/json'
        return GameResponse.from_orm(game).json()


@app.route('/game/<game_id:int>', 'PATCH')
def update_game(game_id: int):
    try:
        game_data = GamePatchRequest(**request.json)
    except ValidationError as e:

        response.status = 400
        return {'error': str(e)}

    with Session() as session:
        is_game_updated = session.query(GameModel).where(
            GameModel.id == game_id
        ).update(game_data.dict(exclude={'days'}))
        if not is_game_updated:
            session.rollback()

            response.status = 404
            return {'error': 'Game not found'}

        for day in game_data.days:
            is_day_updated = session.query(DayModel).where(
                DayModel.game_id == game_id,
                DayModel.number == day.number
            ).update(day.dict(exclude={'number'}))

            if not is_day_updated:
                session.rollback()

                response.status = 404
                return {'error': f'Day with number {day.number} not found'}

        session.commit()


@app.delete('/game/<game_id>')
def delete_game(game_id: int):
    with Session() as session:
        game = session.query(GameModel).where(
            GameModel.id == game_id).one_or_none()
        if game is None:
            response.status = 404
            return {'error': 'Game not found'}

        session.delete(game)
        session.commit()
