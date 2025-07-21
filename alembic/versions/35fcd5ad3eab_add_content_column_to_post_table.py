"""add content column to post table

Revision ID: 35fcd5ad3eab
Revises: 703c492b4050
Create Date: 2025-07-21 10:11:40.274509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35fcd5ad3eab'
down_revision: Union[str, Sequence[str], None] = '703c492b4050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
