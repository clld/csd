"""fix polymorphic_type

Revision ID: 3adce506bfaf
Revises: 
Create Date: 2014-11-26 14:13:38.704000

"""

# revision identifiers, used by Alembic.
revision = '3adce506bfaf'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['language', 'parameter', 'value'], 'base', 'custom')


def downgrade():
    update_pmtype(['language', 'parameter', 'value'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
