"""added JWT blacklist table

Revision ID: 8816a1b74005
Revises: 15f1c5d89d1a
Create Date: 2022-07-14 15:32:20.769731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8816a1b74005'
down_revision = '15f1c5d89d1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token_list')
    # ### end Alembic commands ###
