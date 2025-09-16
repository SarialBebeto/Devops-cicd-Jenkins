"""
Revision ID: 0001_create_users
Revises: 
Create Date: 2025-09-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=128), nullable=False, unique=True),
        sa.Column('active', sa.Boolean, nullable=False, default=True),
    )

def downgrade():
    op.drop_table('users')
