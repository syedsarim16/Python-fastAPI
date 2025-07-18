"""auto-vote

Revision ID: ae514c7f6689
Revises: ddb8780a70a0
Create Date: 2025-07-18 16:20:53.924234
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ae514c7f6689'
down_revision: Union[str, Sequence[str], None] = 'ddb8780a70a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop FK constraint from tasks to users before dropping users
    op.drop_constraint('tasks_owner_id_fkey', 'tasks', type_='foreignkey')

    # Drop indexes and tables
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')

    # Create the votes table
    op.create_table('votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['y_users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )

    # Add owner_id column to posts
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    # Make title and content nullable
    op.alter_column('posts', 'title', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('posts', 'content', existing_type=sa.VARCHAR(), nullable=True)

    # Create FK from posts.owner_id → y_users.id
    op.create_foreign_key('post_y_users_fk', 'posts', 'y_users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # Drop the posts.owner_id FK
    op.drop_constraint('post_y_users_fk', 'posts', type_='foreignkey')

    # Restore content and title nullability
    op.alter_column('posts', 'content', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('posts', 'title', existing_type=sa.VARCHAR(), nullable=False)

    # Remove owner_id from posts
    op.drop_column('posts', 'owner_id')

    # Drop votes table
    op.drop_table('votes')

    # Recreate users table
    op.create_table('users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(), nullable=False),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('password', sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('users_pkey'))
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Recreate tasks table
    op.create_table('tasks',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=True),
        sa.Column('status', postgresql.ENUM('pending', 'in_progress', 'done', name='taskstatus'), nullable=False),
        sa.Column('owner_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='tasks_owner_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='tasks_pkey')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
