import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Load Alembic config file
config = context.config

# Set up logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """Get SQLAlchemy database URL and ensure it's formatted correctly."""
    try:
        engine = get_engine()
        if engine and engine.url:
            return get_engine().url.render_as_string(hide_password=False).replace(
        'postgres://', 'postgresql://'
    )
        else:
            raise ValueError("Database URL is missing!")
    except AttributeError:
        logger.error("Error fetching database URL. Ensure the app is configured properly.")
        return ""  # Return an empty string to avoid crashes

   

# Set database URL for Alembic
config.set_main_option('sqlalchemy.url', get_engine_url())

target_db = current_app.extensions['migrate'].db

def get_metadata():
    """Fetch metadata for autogeneration."""
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas.get(None, target_db.metadata)
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in offline mode (without a database connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in online mode (with a database connection)."""

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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

