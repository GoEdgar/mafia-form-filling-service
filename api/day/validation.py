from pydantic import conlist

from api.common import BaseValidator


class VotingObject(BaseValidator):
    player_id: int
    who_put_to_vote_id: int
    first_vote_count: int
    second_vote_count: int


class GameDayBase(BaseValidator):
    number: int
    voting_map: conlist(VotingObject, min_items=0, max_items=1) = []


class GameDayCreateRequest(GameDayBase):
    game_id: int


class GameDayInlineCreateRequest(GameDayBase):
    pass

class GameDayPatchRequest(GameDayBase):
    game_id: int
    number: int = None


class GameDayResponse(GameDayBase):
    game_id: int
