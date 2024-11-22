"""Create users and rates tables

Revision ID: 000
Revises:
Create Date: 2024-11-21 15:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('rates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.Column('cargo_type', sa.String(), nullable=False),
                    sa.Column('rate', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('rates')
    op.drop_table('users')
