"""add none to entityid

Revision ID: f8d4f557e526
Revises: 5a4fb7da7018
Create Date: 2022-11-01 20:37:30.767536

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'f8d4f557e526'
down_revision = '5a4fb7da7018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
