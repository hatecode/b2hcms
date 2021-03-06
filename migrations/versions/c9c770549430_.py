"""empty message

Revision ID: c9c770549430
Revises: b5df1a6243da
Create Date: 2019-02-16 22:46:55.387614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9c770549430'
down_revision = 'b5df1a6243da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('operationlogs', sa.Column('actioncontent', sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('operationlogs', 'actioncontent')
    # ### end Alembic commands ###
