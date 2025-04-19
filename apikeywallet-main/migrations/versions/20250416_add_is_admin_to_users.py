"""
Add is_admin column to users table
"""

# revision identifiers, used by Alembic.
revision = '20250416_add_is_admin_to_users'
down_revision = '81699dd1d304'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))

def downgrade():
    op.drop_column('user', 'is_admin')
