import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
from alembic import op  # Import op for migration operations
import sqlalchemy as sa
from sqlalchemy.engine import reflection
from sqlalchemy.exc import ProgrammingError  # Import the error for handling

# Load Alembic config file
config = context.config

# Set up logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Function to handle the upgrade (applying migrations)

# Function to check if the table exists
def table_exists(table_name):
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    return table_name in inspector.get_table_names()

def upgrade():
    # Check if the table 'mutare_submission' exists before attempting to drop it
    if table_exists('mutare_submission'):
        try:
           # op.drop_table('mutare_submission')#
            print("Table 'mutare_submission' dropped.")
        except ProgrammingError as e:
            print(f"Error dropping table 'mutare_submission': {e}")
    else:
        print("Table 'mutare_submission' does not exist. Skipping drop operation.")

def downgrade():
    # You can optionally define the reverse of this migration here
    pass

# Get engine for Alembic
def get_engine():
    try:
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions['migrate'].db.engine

# Get database URL
def get_engine_url():
    """Get SQLAlchemy database URL and ensure it's formatted correctly."""
    try:
        db_uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if not db_uri:
            raise ValueError("SQLALCHEMY_DATABASE_URI is missing. Ensure DATABASE_URL is set.")
        return db_uri.replace("postgres://", "postgresql://")
    except Exception as e:
        logger.error(f"Error fetching database URL: {e}")
        return ""

# Set database URL for Alembic
config.set_main_option('sqlalchemy.url', get_engine_url())

# Get metadata for Alembic's autogeneration
target_db = current_app.extensions['migrate'].db

def get_metadata():
    """Fetch metadata for autogeneration."""
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas.get(None, target_db.metadata)
    return target_db.metadata

# Run migrations in offline mode (without a database connection)
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

# Run migrations in online mode (with a database connection)
def run_migrations_online():
    def process_revision_directives(context, revision, directives):
       if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    conf_args.setdefault("process_revision_directives", process_revision_directives)

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=get_metadata(), **conf_args)

        with context.begin_transaction():
            context.run_migrations()

# Run migrations based on mode (offline or online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

