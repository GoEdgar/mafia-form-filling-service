from pydantic import conlist

from api.common import Validator


class VotingMap(Validator):
    # [[player_id, who_put_to_vote_id, first_vote_count, second_vote_count], ...]
    voting_map: conlist(conlist(int, min_items=4, max_items=4), min_items=1,
                        max_items=10) = None


class GameDayBase(VotingMap):
    game_id: int
    number: int


class GameDayCreate(GameDayBase):
    game_id: int = None


class GameDayPatchRequest(VotingMap):
    number: int = None


class GameDayResponse(GameDayBase, VotingMap):
    pass
