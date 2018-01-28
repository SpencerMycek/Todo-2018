"""todo completed

Revision ID: 1a7a10335ae3
Revises: 5c4725f70af3
Create Date: 2018-01-28 00:56:29.003332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a7a10335ae3'
down_revision = '5c4725f70af3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('completed', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_todo_completed'), 'todo', ['completed'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todo_completed'), table_name='todo')
    op.drop_column('todo', 'completed')
    # ### end Alembic commands ###
