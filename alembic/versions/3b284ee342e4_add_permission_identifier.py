"""add Permission identifier

Revision ID: 3b284ee342e4
Revises: d0c6730e635f
Create Date: 2019-12-27 10:24:34.579916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b284ee342e4'
down_revision = 'd0c6730e635f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permission', sa.Column('identifier', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permission', 'identifier')
    # ### end Alembic commands ###
