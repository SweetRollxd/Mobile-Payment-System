"""Added quantity to purchase_product table

Revision ID: 4dcef3c4afdf
Revises: bae5a74ee990
Create Date: 2022-11-12 22:55:20.533747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dcef3c4afdf'
down_revision = 'bae5a74ee990'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase_product', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchase_product', 'quantity')
    # ### end Alembic commands ###
