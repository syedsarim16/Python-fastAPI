"""add foreign-key to posts table

Revision ID: 60f2955a5e5b
Revises: 62991d8d0257
Create Date: 2025-07-18 15:34:05.658634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '60f2955a5e5b'
down_revision: Union[str, Sequence[str], None] = '62991d8d0257'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Add the owner_id column to posts table
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    # Create the foreign key from posts.owner_id → y_users.id
    op.create_foreign_key(
        'post_y_users_fk',              # FK constraint name
        source_table='posts',
        referent_table='y_users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    conn = op.get_bind()
    result = conn.execute(text("""
        SELECT 1 FROM pg_constraint
        WHERE conname = 'post_y_users_fk' AND conrelid = 'posts'::regclass
    """))
    if result.fetchone():
        op.drop_constraint('post_y_users_fk', 'posts', type_='foreignkey')
    
    op.drop_column('posts', 'owner_id')
