"""auto-generate the transaction table

Revision ID: 5410cc182f1e
Revises: f7a59f10f0b4
Create Date: 2022-01-29 17:47:10.821042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5410cc182f1e'
down_revision = 'f7a59f10f0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(timezone=True), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.Column('label_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('notes', sa.String(), nullable=False),
    sa.Column('transaction_type', sa.Enum('Income', 'Expense', name='transactiontype'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###
