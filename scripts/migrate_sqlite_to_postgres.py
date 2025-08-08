#!/usr/bin/env python3
"""
Non-destructive migration from SQLite to PostgreSQL.

Usage:
  SQLITE_DB=apikeywallet-main/app.db \
  DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db \
  python scripts/migrate_sqlite_to_postgres.py

This script:
  - Reflects models via SQLAlchemy ORM
  - Creates tables in Postgres if not present
  - Copies rows table-by-table preserving IDs
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath('apikeywallet-main'))
from models import User, APIKey, Category  # type: ignore
from app import db  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sqlite_to_pg")

sqlite_path = os.environ.get('SQLITE_DB', 'apikeywallet-main/app.db')
pg_url = os.environ.get('DATABASE_URL')
if not pg_url:
    raise SystemExit("DATABASE_URL is required for Postgres target")

sqlite_url = f"sqlite:///{sqlite_path}"

sqlite_engine = create_engine(sqlite_url)
pg_engine = create_engine(pg_url)

SqliteSession = sessionmaker(bind=sqlite_engine)
PgSession = sessionmaker(bind=pg_engine)

def copy_table(model):
    src = SqliteSession()
    dst = PgSession()
    try:
        logger.info("Copying %s...", model.__tablename__)
        # Ensure target tables exist
        model.metadata.create_all(pg_engine, tables=[model.__table__])
        rows = src.query(model).all()
        for row in rows:
            data = {c.name: getattr(row, c.name) for c in model.__table__.columns}
            # Upsert by primary key id
            placeholders = ', '.join(f':{k}' for k in data.keys())
            columns = ', '.join(data.keys())
            update_set = ', '.join(f"{k}=excluded.{k}" for k in data.keys() if k != 'id')
            insert_sql = f"""
                INSERT INTO {model.__tablename__} ({columns})
                VALUES ({placeholders})
                ON CONFLICT (id) DO UPDATE SET {update_set}
            """
            dst.execute(text(insert_sql), data)
        dst.commit()
        logger.info("Copied %d rows into %s", len(rows), model.__tablename__)
    finally:
        src.close()
        dst.close()

def main():
    # Order: parent tables first
    copy_table(User)
    copy_table(Category)
    copy_table(APIKey)
    logger.info("Migration complete")

if __name__ == '__main__':
    main()


