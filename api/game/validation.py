from datetime import datetime, timezone
from enum import Enum

from pydantic import conlist

from api.common import BaseValidator
from api.day.validation import GameDayBase, GameDayInlineCreateRequest


class StatusEnum(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class WhoIsWonEnum(str, Enum):
    RED = 'RED'
    BLACK = 'BLACK'
    DRAW = 'DRAW'


class GameBase(BaseValidator):
    host_id: int = None
    best_move: list[int] = None
    start_datetime: datetime = None
    end_datetime: datetime = None
    status: StatusEnum = None
    won: WhoIsWonEnum = None
    note: str = None

    black_player_one_id: int = None
    black_player_two_id: int = None
    don_player_id: int = None
    sheriff_player_id: int = None
    first_shoot_player_id: int = None

    # [[player_id, foul_count], ...]
    players: conlist(conlist(int, min_items=2, max_items=2),
                     min_items=10, max_items=10) = None

    # [[player_id, additional_points], ...]
    best_players: conlist(conlist(float, min_items=2, max_items=2),
                          min_items=0, max_items=10) = None

    inserted_at: datetime = None


class GameCreateRequest(GameBase):
    creator_id: int
    number: int

    days: list[GameDayInlineCreateRequest] = []


class GamePatchRequest(GameBase):
    number: int = None

    is_aggregated: bool = None
    updated_at: datetime = None
    # days: list[GameDayPatchRequest] = []


class GameResponse(GameBase):
    id: int
    number: int
    creator_id: int
    host_id: int = None
    is_aggregated: bool = None
    updated_at: datetime = None

    days: list[GameDayBase] = []


class GameListResponse(BaseValidator):
    games: list[GameResponse]
    games_count: int


def validate_game_constraints(game):
    # all user ids are unique constraint
    if game.players:
        unique_ids = {
            game.host_id or game.creator_id,
            *(player[0] for player in game.players),
        }
        if len(unique_ids) < len(game.players) + 1:
            raise ValueError("There are duplicates around players and host")

    # start_datetime < end_datetime constraint
    if all((game.start_datetime, game.end_datetime)) \
            and game.start_datetime.replace(tzinfo=timezone.utc) \
            >= game.end_datetime.replace(tzinfo=timezone.utc):
        raise ValueError("start_datetime should be greater than end_datetime")
