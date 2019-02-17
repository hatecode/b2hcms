"""empty message

Revision ID: d4bc619881c2
Revises: c9c770549430
Create Date: 2019-02-17 16:02:46.249427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4bc619881c2'
down_revision = 'c9c770549430'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('operationlogs', sa.Column('remote_addr', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_operationlogs_remote_addr'), 'operationlogs', ['remote_addr'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_operationlogs_remote_addr'), table_name='operationlogs')
    op.drop_column('operationlogs', 'remote_addr')
    # ### end Alembic commands ###
