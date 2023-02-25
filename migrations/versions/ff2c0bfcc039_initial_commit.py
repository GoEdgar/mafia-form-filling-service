"""Initial commit

Revision ID: ff2c0bfcc039
Revises: 
Create Date: 2023-02-25 19:46:32.488260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff2c0bfcc039'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('best_move', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('start_datetime', sa.DateTime(), nullable=True),
    sa.Column('end_datetime', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('IN_PROGRESS', 'COMPLETED', name='statusenum'), nullable=True),
    sa.Column('won', sa.Enum('RED', 'BLACK', name='whoiswonenum'), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('black_player_one_id', sa.Integer(), nullable=True),
    sa.Column('black_player_two_id', sa.Integer(), nullable=True),
    sa.Column('don_player_id', sa.Integer(), nullable=True),
    sa.Column('sheriff_player_id', sa.Integer(), nullable=True),
    sa.Column('first_shoot_player_id', sa.Integer(), nullable=True),
    sa.Column('players', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('best_players', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('is_aggregated', sa.Boolean(), nullable=True),
    sa.Column('inserted_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('day',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('voting_map', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('game_id', 'number', name='_unique_day_number_per_game')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('day')
    op.drop_table('game')
    # ### end Alembic commands ###
