from pydantic import conlist

from api.common import Validator

class VotingObject(Validator):
    player_id: int
    who_put_to_vote_id: int
    first_vote_count: int
    second_vote_count: int

class VotingMap(Validator):
    voting_map: conlist(VotingObject, min_items=1, max_items=1) = None


class GameDayBase(VotingMap):
    game_id: int
    number: int


class GameDayCreate(GameDayBase):
    game_id: int = None


class GameDayPatchRequest(VotingMap):
    number: int = None


class GameDayResponse(GameDayBase, VotingMap):
    pass
