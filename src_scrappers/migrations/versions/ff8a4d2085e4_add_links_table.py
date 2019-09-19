"""add_links_table

Revision ID: ff8a4d2085e4
Revises: 
Create Date: 2019-09-19 16:08:57.476496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8a4d2085e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'music',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('link', sa.VARCHAR(256)),
        sa.Column('hash_link', sa.VARCHAR(16), unique=True),
        sa.Column('name', sa.VARCHAR(64)),
        sa.Column('genre', sa.VARCHAR(16)),
        sa.Column('duration', sa.INTEGER, default=0),
        sa.Column('download_link', sa.VARCHAR(256)),
        sa.Column('status', sa.SMALLINT, default=0),

        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text(
            'CURRENT_TIMESTAMP'), nullable=False),
        sa.Column(
            'updated_at', sa.TIMESTAMP(),
            server_default=sa.text(
                'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
            nullable=False
        )
    )
    op.create_index('ik_music', 'music',
                    ['hash_link', 'duration', 'download_link'])


def downgrade():
    op.drop_table('music')
