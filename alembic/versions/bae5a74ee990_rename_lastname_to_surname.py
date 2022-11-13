"""Rename lastname to surname

Revision ID: bae5a74ee990
Revises: 4a4ac4eab226
Create Date: 2022-11-12 15:48:58.844859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bae5a74ee990'
down_revision = '4a4ac4eab226'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appuser', sa.Column('surname', sa.String(), nullable=True))
    op.drop_column('appuser', 'lastname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appuser', sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('appuser', 'surname')
    # ### end Alembic commands ###