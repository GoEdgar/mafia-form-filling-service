from datetime import datetime
from enum import Enum

import pydantic
from pydantic import conlist

from api.common import Validator
from api.day.validation import GameDayCreate, GameDayBase, GameDayPatchRequest


class StatusEnum(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class WhoIsWonEnum(str, Enum):
    RED = 'RED'
    BLACK = 'BLACK'
    DRAW = 'DRAW'


class GameBase(Validator):
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
                          min_items=10, max_items=10) = None

    inserted_at: datetime = None

    @pydantic.root_validator()
    @classmethod
    def validate_unique_user_ids(cls, field_values):
        if field_values["players"]:
            unique_ids = {
                field_values["host_id"],
                *(player[0] for player in field_values["players"]),
                }
            if len(unique_ids) < len(field_values["players"]) + 1:
                raise ValueError("There are duplicates around players and host")

        return field_values


class GameCreateRequest(GameBase):
    host_id: int
    number: int

    days: list[GameDayCreate] = []


class GamePatchRequest(GameBase):
    host_id: int = None
    number: int = None

    is_aggregated: bool = None
    updated_at: datetime = None
    # days: list[GameDayPatchRequest] = []


class GameResponse(GameBase):
    id: int
    host_id: int
    number: int
    is_aggregated: bool = None
    updated_at: datetime = None

    days: list[GameDayBase] = []
