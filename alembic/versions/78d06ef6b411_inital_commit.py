"""inital commit

Revision ID: 78d06ef6b411
Revises:
Create Date: 2022-06-09 13:34:37.325035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d06ef6b411'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table('users',
    sa.Column('id', sa.Integer, primary_key=True,  nullable=False),
    sa.Column('first_name', sa.String(255), nullable=False),
    sa.Column('last_name', sa.String(255), nullable=False),
    sa.Column('email', sa.String(100), nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
              server_default=sa.text('now()'), nullable=False),
    sa.Column('last_login', sa.TIMESTAMP(timezone=True)),

    sa.UniqueConstraint('email')
    )
    
    op.create_table('supplies',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('item_name', sa.String(255), nullable=False),
    sa.Column('quantity', sa.Integer, nullable=False),
    sa.Column('date_ordered', sa.DateTime, nullable=False),
    sa.Column('order_status', sa.String),
    sa.Column('temp_sensitive', sa.String(20)),
    sa.Column('recieved_by', sa.String(255)),
    sa.Column('users_id', sa.Integer()),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
    
    )
    
    op.create_foreign_key("supplies_users_fk", source_table="supplies", referent_table="users", local_cols=["users_id"], remote_cols=['id'])


def downgrade():

    op.drop_table('users')
    op.drop_table('supplies')
    op.drop_constraint('supplies_users_fk', table_name="supplies")
