from pathlib import Path

import pandas as pd
from sqlalchemy import text

from fund_finance.db.connection import get_engine

RAW_DATA_DIR = Path("data/raw")

LOAD_ORDER = [
    "fund_managers",
    "funds",
    "investors",
    "capital_commitments",
    "capital_calls",
    "nav_history",
    "portfolio_companies",
    "facility_terms",
    "covenant_terms",
    "monitoring_events",
]

DATE_COLUMNS = {
    "funds": ["investment_period_end", "fund_term_end"],
    "capital_commitments": ["commitment_date"],
    "capital_calls": ["call_date", "due_date"],
    "nav_history": ["reporting_date"],
    "portfolio_companies": ["investment_date", "last_round_date"],
    "facility_terms": ["maturity_date"],
    "monitoring_events": ["event_date"],
}


def _clean_dataframe(table_name: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean CSV data before loading into PostgreSQL."""
    dataframe = dataframe.copy()

    # Convert blank strings to NULL.
    dataframe = dataframe.replace({"": None})

    # Convert known date columns to Python date objects.
    for column in DATE_COLUMNS.get(table_name, []):
        if column in dataframe.columns:
            dataframe[column] = pd.to_datetime(dataframe[column], errors="coerce").dt.date
            dataframe[column] = dataframe[column].where(dataframe[column].notna(), None)

    return dataframe


def load_table(table_name: str) -> int:
    """Load a single CSV file into the matching PostgreSQL table."""
    csv_path = RAW_DATA_DIR / f"{table_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing required input file: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    dataframe = _clean_dataframe(table_name, dataframe)

    engine = get_engine()

    with engine.begin() as connection:
        dataframe.to_sql(
            table_name,
            con=connection,
            if_exists="append",
            index=False,
            method="multi",
        )

    return len(dataframe)


def reset_loaded_tables() -> None:
    """Clear loaded data while preserving the database schema."""
    engine = get_engine()

    tables = ", ".join(LOAD_ORDER)

    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE;"))


def load_all_raw_data(reset: bool = True) -> dict[str, int]:
    """Load all raw CSV files into PostgreSQL in foreign-key-safe order."""
    if reset:
        reset_loaded_tables()

    row_counts = {}

    for table_name in LOAD_ORDER:
        row_counts[table_name] = load_table(table_name)

    return row_counts


def count_loaded_rows() -> dict[str, int]:
    """Return row counts for all loaded tables."""
    engine = get_engine()
    row_counts = {}

    with engine.connect() as connection:
        for table_name in LOAD_ORDER:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
            row_counts[table_name] = int(result.scalar_one())

    return row_counts
