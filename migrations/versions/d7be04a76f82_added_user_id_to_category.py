"""Added user_id to category

Revision ID: d7be04a76f82
Revises: 39f74cfac400
Create Date: 2024-05-19 16:19:26.598643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7be04a76f82'
down_revision = '39f74cfac400'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_category_user_id', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_constraint('fk_category_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###