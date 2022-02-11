"""add on-delete constraint to transaction_label table

Revision ID: f7f45f3360a8
Revises: 98c847e45036
Create Date: 2022-02-11 14:02:34.508672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f45f3360a8'
down_revision = '98c847e45036'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('transaction_labels_transaction_id_fkey', 'transaction_labels', type_='foreignkey')
    op.create_foreign_key(None, 'transaction_labels', 'transactions', ['transaction_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction_labels', type_='foreignkey')
    op.create_foreign_key('transaction_labels_transaction_id_fkey', 'transaction_labels', 'transactions', ['transaction_id'], ['id'])
    # ### end Alembic commands ###
