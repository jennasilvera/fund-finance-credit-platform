from pathlib import Path

import pytest

from fund_finance.db.connection import get_engine
from fund_finance.db.load import load_all_raw_data
from fund_finance.etl.generate_sample_data import generate_all


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    """Rebuild schema and reload sample data before the test suite runs."""
    schema_path = Path("sql/schema.sql")
    schema_sql = schema_path.read_text()

    engine = get_engine()

    raw_connection = engine.raw_connection()
    try:
        cursor = raw_connection.cursor()
        cursor.execute(schema_sql)
        raw_connection.commit()
    finally:
        raw_connection.close()

    generate_all()
    load_all_raw_data(reset=True)
