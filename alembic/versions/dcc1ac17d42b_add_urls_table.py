"""Add urls table

Revision ID: dcc1ac17d42b
Revises: 
Create Date: 2018-11-20 23:09:01.729361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dcc1ac17d42b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "urls",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("url", sa.String(), nullable=False),
    )


def downgrade():
    pass
