"""add foreign-key to post table

Revision ID: bdfa422af40c
Revises: e51c9579139d
Create Date: 2025-07-21 10:29:02.033905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdfa422af40c'
down_revision: Union[str, Sequence[str], None] = 'e51c9579139d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                         local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
