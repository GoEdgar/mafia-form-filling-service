"""constraint start_dt < end_dt

Revision ID: 82bab8395a0a
Revises: 7bf99c913b2e
Create Date: 2023-04-09 23:33:56.464160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82bab8395a0a'
down_revision = '7bf99c913b2e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        "start_dt_greater_than_end_dt",
        "game",
        "start_datetime < end_datetime",
        )


def downgrade() -> None:
    op.drop_constraint(
        "start_dt_greater_than_end_dt",
        "game",
        )
