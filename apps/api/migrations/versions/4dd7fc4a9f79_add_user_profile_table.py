"""Add user profile table

Revision ID: 4dd7fc4a9f79
Revises: 
Create Date: 2025-07-09 05:52:26.304082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dd7fc4a9f79'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('favorite_food', sa.String(length=100), nullable=True),
    sa.Column('hobbies', sa.Text(), nullable=True),
    sa.Column('job', sa.String(length=100), nullable=True),
    sa.Column('color_preferences', sa.Text(), nullable=True),
    sa.Column('material_preferences', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profiles')
    # ### end Alembic commands ###
