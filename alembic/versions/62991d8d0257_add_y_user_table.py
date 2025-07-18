"""add y_user table

Revision ID: 62991d8d0257
Revises: a924f8de2b05
Create Date: 2025-07-18 14:57:27.473394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62991d8d0257'
down_revision: Union[str, Sequence[str], None] = 'a924f8de2b05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('y_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
              server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
)
    pass


def downgrade() -> None:
   op.drop_table('y_users')
pass
