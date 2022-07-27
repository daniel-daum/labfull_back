"""added last_modified_column to supplies table

Revision ID: 026bde5d969c
Revises: a3e57a367968
Create Date: 2022-07-22 21:41:15.276107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '026bde5d969c'
down_revision = 'a3e57a367968'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('supplies', sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('supplies', 'last_modified_at')
    # ### end Alembic commands ###