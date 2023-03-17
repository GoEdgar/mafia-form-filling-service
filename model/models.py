from sqlalchemy import (Column, Integer, Float, ForeignKey, ARRAY, DateTime,
                        Enum, String,
                        Boolean, UniqueConstraint, JSON)
from sqlalchemy.orm import relationship

from api.game.validation import StatusEnum, WhoIsWonEnum
from model import Base


class DayModel(Base):
    __tablename__ = 'day'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('GameModel', back_populates='days')
    number = Column(Integer)

    voting_map = Column(JSON)

    __table_args__ = (
        UniqueConstraint('game_id', 'number',
                         name='_unique_day_number_per_game'),
    )


class GameModel(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer)
    number = Column(Integer)
    best_move = Column(ARRAY(Integer))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    status = Column(Enum(StatusEnum))
    won = Column(Enum(WhoIsWonEnum))
    note = Column(String)

    black_player_one_id = Column(Integer)
    black_player_two_id = Column(Integer)
    don_player_id = Column(Integer)
    sheriff_player_id = Column(Integer)
    first_shoot_player_id = Column(Integer)

    players = Column(ARRAY(Integer))
    days = relationship('DayModel')
    best_players = Column(ARRAY(Float))

    is_aggregated = Column(Boolean, default=False)
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)
