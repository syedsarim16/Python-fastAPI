"""add user table

Revision ID: e51c9579139d
Revises: 35fcd5ad3eab
Create Date: 2025-07-21 10:16:30.137134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e51c9579139d'
down_revision: Union[str, Sequence[str], None] = '35fcd5ad3eab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table('users',
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
    op.drop_table('users')
    pass
