from datetime import datetime
from enum import Enum

from pydantic import conlist

from api.common import Validator
from api.day.validation import GameDayCreate, GameDayBase, GameDayPatchRequest


class StatusEnum(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class WhoIsWonEnum(str, Enum):
    RED = 'RED'
    BLACK = 'BLACK'


class GameBase(Validator):
    best_move: list[int] = None
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
                     min_items=2, max_items=2) = None

    # [[player_id, additional_points], ...]
    best_players: conlist(conlist(float, min_items=2, max_items=2),
                          min_items=2, max_items=2) = None


class GameCreateRequest(GameBase):
    host_id: int
    number: int

    days: list[GameDayCreate] = []


class GamePatchRequest(GameBase):
    number: int = None
    start_datetime: datetime = None

    days: list[GameDayPatchRequest] = []


class GameResponse(GameBase):
    id: int
    host_id: int
    number: int
    start_datetime: datetime
    is_aggregated: bool = None
    inserted_at: datetime = None
    updated_at: datetime = None

    days: list[GameDayBase] = []
