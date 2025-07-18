"""add content column to posts table

Revision ID: a924f8de2b05
Revises: 1f68ff390435
Create Date: 2025-07-18 14:49:19.534395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a924f8de2b05'
down_revision: Union[str, Sequence[str], None] = '1f68ff390435'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
