from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import Base, sync_engine  # ← Bu sening loyiha strukturangga mos bo'lishi kerak
from core.models import *  # barcha modellaringni shu yerga import qilgan bo'lishing kerak

# Alembic Config object
config = context.config

# Logging
fileConfig(config.config_file_name)

# target_metadata aytilganidek model metadatasini olamiz
target_metadata = Base.metadata


def run_migrations_offline():
    """Offline rejimda migration yaratish."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online rejimda migration yaratish."""
    connectable = sync_engine  # create_engine emas, sening bazangdan

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
