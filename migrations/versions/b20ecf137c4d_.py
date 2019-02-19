"""empty message

Revision ID: b20ecf137c4d
Revises: d4bc619881c2
Create Date: 2019-02-19 23:26:36.903850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b20ecf137c4d'
down_revision = 'd4bc619881c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operatorslogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=15), nullable=False),
    sa.Column('actiontype', sa.String(length=10), nullable=False),
    sa.Column('actiontime', sa.DateTime(), nullable=True),
    sa.Column('actioncontent', sa.UnicodeText(), nullable=True),
    sa.Column('user', sa.String(length=30), nullable=False),
    sa.Column('remote_addr', sa.String(length=20), nullable=True),
    sa.Column('filetype', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operatorslogs_actiontype'), 'operatorslogs', ['actiontype'], unique=False)
    op.create_index(op.f('ix_operatorslogs_filename'), 'operatorslogs', ['filename'], unique=False)
    op.create_index(op.f('ix_operatorslogs_filetype'), 'operatorslogs', ['filetype'], unique=False)
    op.create_index(op.f('ix_operatorslogs_remote_addr'), 'operatorslogs', ['remote_addr'], unique=False)
    op.create_index(op.f('ix_operatorslogs_user'), 'operatorslogs', ['user'], unique=False)
    op.create_index(op.f('ix_operationlogs_remote_addr'), 'operationlogs', ['remote_addr'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_operationlogs_remote_addr'), table_name='operationlogs')
    op.drop_index(op.f('ix_operatorslogs_user'), table_name='operatorslogs')
    op.drop_index(op.f('ix_operatorslogs_remote_addr'), table_name='operatorslogs')
    op.drop_index(op.f('ix_operatorslogs_filetype'), table_name='operatorslogs')
    op.drop_index(op.f('ix_operatorslogs_filename'), table_name='operatorslogs')
    op.drop_index(op.f('ix_operatorslogs_actiontype'), table_name='operatorslogs')
    op.drop_table('operatorslogs')
    # ### end Alembic commands ###
