from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from fund_finance.config.settings import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True)


def test_connection() -> str:
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        return str(result.scalar_one())


def list_tables() -> list[str]:
    engine = get_engine()

    query = text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)
        return [row[0] for row in result.fetchall()]
