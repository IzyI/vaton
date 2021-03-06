""" VUserInfo add id_user

Revision ID: a3df2387d145
Revises: bf75cdb81160
Create Date: 2022-05-06 13:50:02.178915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3df2387d145'
down_revision = 'bf75cdb81160'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vaton_user_info', sa.Column('id_user', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'vaton_user_info', 'vaton_user', ['id_user'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vaton_user_info', type_='foreignkey')
    op.drop_column('vaton_user_info', 'id_user')
    # ### end Alembic commands ###
