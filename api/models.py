from sqlalchemy import (Column, Integer, ForeignKey, ARRAY, DateTime, Enum, String,
                        Boolean, UniqueConstraint)
from sqlalchemy.orm import relationship

from db import Base
from game.validation import StatusEnum, WhoIsWonEnum


class DayModel(Base):
    __tablename__ = "day"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("GameModel", back_populates="days")
    number = Column(Integer)

    voting_map = Column(ARRAY(Integer))

    __table_args__ = (
    UniqueConstraint('game_id', 'number', name='_unique_day_number_per_game'),
    )


class GameModel(Base):
    __tablename__ = "game"

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
    days = relationship("DayModel")
    best_players = Column(ARRAY(Integer))

    is_aggregated = Column(Boolean)
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)
