"""newMigration

Revision ID: bb781ade149b
Revises: 843851554271
Create Date: 2021-07-25 22:50:22.215565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb781ade149b'
down_revision = '843851554271'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('debian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=40), nullable=True),
    sa.Column('country_name', sa.String(length=40), nullable=True),
    sa.Column('disk', sa.String(length=40), nullable=True),
    sa.Column('filesystem', sa.String(length=40), nullable=True),
    sa.Column('guided_size', sa.String(length=40), nullable=True),
    sa.Column('install_addition', sa.String(length=40), nullable=True),
    sa.Column('interface', sa.String(length=40), nullable=True),
    sa.Column('language', sa.String(length=40), nullable=True),
    sa.Column('language_name_fb', sa.String(length=40), nullable=True),
    sa.Column('layoutcode', sa.String(length=40), nullable=True),
    sa.Column('locale', sa.String(length=40), nullable=True),
    sa.Column('method', sa.String(length=40), nullable=True),
    sa.Column('multi_language_environment', sa.String(length=40), nullable=True),
    sa.Column('xkbkeymap', sa.String(length=40), nullable=True),
    sa.Column('partition_method', sa.String(length=40), nullable=True),
    sa.Column('recipe', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('windows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('execution_policy', sa.String(length=3), nullable=True),
    sa.Column('quick_config', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('windows')
    op.drop_table('debian')
    # ### end Alembic commands ###
