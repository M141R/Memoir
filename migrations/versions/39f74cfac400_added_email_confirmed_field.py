"""Added email_confirmed field

Revision ID: 39f74cfac400
Revises: 
Create Date: 2024-05-14 10:52:16.624917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39f74cfac400'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.engine.reflection.Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('user')]
    if 'email_confirmed' not in columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('email_confirmed', sa.Boolean(), nullable=True))


def downgrade():
    conn = op.get_bind()
    inspector = sa.engine.reflection.Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('user')]
    if 'email_confirmed' in columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.drop_column('email_confirmed')
