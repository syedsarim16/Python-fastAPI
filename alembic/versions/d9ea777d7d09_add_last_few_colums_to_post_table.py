"""add last few colums to post table 

Revision ID: d9ea777d7d09
Revises: bdfa422af40c
Create Date: 2025-07-21 10:35:02.211934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9ea777d7d09'
down_revision: Union[str, Sequence[str], None] = 'bdfa422af40c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE',))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text(
        'NOW()',),))
    pass

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
