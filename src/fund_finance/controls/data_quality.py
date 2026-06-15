from dataclasses import dataclass
from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw")


@dataclass
class DataQualityIssue:
    table_name: str
    check_name: str
    severity: str
    message: str


REQUIRED_FILES = {
    "fund_managers": ["manager_id", "manager_name", "sponsor_risk_rating"],
    "funds": [
        "fund_id",
        "manager_id",
        "fund_name",
        "committed_capital_usd",
        "called_capital_usd",
        "uncalled_capital_usd",
        "nav_usd",
    ],
    "investors": [
        "investor_id",
        "investor_name",
        "investor_category",
        "included_in_borrowing_base_flag",
    ],
    "capital_commitments": [
        "commitment_id",
        "fund_id",
        "investor_id",
        "commitment_amount_usd",
        "called_amount_usd",
        "uncalled_amount_usd",
        "default_status",
    ],
    "capital_calls": [
        "capital_call_id",
        "fund_id",
        "investor_id",
        "call_date",
        "due_date",
        "amount_called_usd",
        "amount_funded_usd",
        "status",
    ],
    "nav_history": ["nav_id", "fund_id", "reporting_date", "gross_nav_usd", "net_nav_usd"],
    "portfolio_companies": [
        "company_id",
        "fund_id",
        "company_name",
        "sector",
        "current_fair_value_usd",
    ],
    "facility_terms": [
        "facility_id",
        "fund_id",
        "facility_type",
        "commitment_amount_usd",
        "outstanding_amount_usd",
    ],
    "covenant_terms": [
        "covenant_id",
        "facility_id",
        "covenant_name",
        "threshold_value",
    ],
    "monitoring_events": ["event_id", "fund_id", "facility_id", "event_date", "severity"],
}


PRIMARY_KEYS = {
    "fund_managers": "manager_id",
    "funds": "fund_id",
    "investors": "investor_id",
    "capital_commitments": "commitment_id",
    "capital_calls": "capital_call_id",
    "nav_history": "nav_id",
    "portfolio_companies": "company_id",
    "facility_terms": "facility_id",
    "covenant_terms": "covenant_id",
    "monitoring_events": "event_id",
}


def _issue(table_name: str, check_name: str, message: str) -> DataQualityIssue:
    return DataQualityIssue(
        table_name=table_name,
        check_name=check_name,
        severity="high",
        message=message,
    )


def _read_csv(raw_data_dir: Path, table_name: str) -> pd.DataFrame | None:
    path = raw_data_dir / f"{table_name}.csv"

    if not path.exists():
        return None

    return pd.read_csv(path)


def _check_required_files_and_columns(raw_data_dir: Path) -> list[DataQualityIssue]:
    issues = []

    for table_name, required_columns in REQUIRED_FILES.items():
        dataframe = _read_csv(raw_data_dir, table_name)

        if dataframe is None:
            issues.append(
                _issue(
                    table_name=table_name,
                    check_name="required_file_exists",
                    message=f"Missing required file {table_name}.csv",
                )
            )
            continue

        missing_columns = [
            column for column in required_columns if column not in dataframe.columns
        ]

        if missing_columns:
            issues.append(
                _issue(
                    table_name=table_name,
                    check_name="required_columns_exist",
                    message=f"Missing required columns: {', '.join(missing_columns)}",
                )
            )

    return issues


def _check_primary_keys(raw_data_dir: Path) -> list[DataQualityIssue]:
    issues = []

    for table_name, primary_key in PRIMARY_KEYS.items():
        dataframe = _read_csv(raw_data_dir, table_name)

        if dataframe is None or primary_key not in dataframe.columns:
            continue

        if dataframe[primary_key].isna().any():
            issues.append(
                _issue(
                    table_name=table_name,
                    check_name="primary_key_not_null",
                    message=f"{primary_key} contains null values",
                )
            )

        duplicate_count = int(dataframe[primary_key].duplicated().sum())

        if duplicate_count > 0:
            issues.append(
                _issue(
                    table_name=table_name,
                    check_name="primary_key_unique",
                    message=f"{primary_key} contains {duplicate_count} duplicate values",
                )
            )

    return issues


def _check_fund_capital_math(raw_data_dir: Path) -> list[DataQualityIssue]:
    dataframe = _read_csv(raw_data_dir, "funds")
    issues = []

    if dataframe is None:
        return issues

    required = {"committed_capital_usd", "called_capital_usd", "uncalled_capital_usd"}

    if not required.issubset(dataframe.columns):
        return issues

    committed = pd.to_numeric(dataframe["committed_capital_usd"], errors="coerce")
    called = pd.to_numeric(dataframe["called_capital_usd"], errors="coerce")
    uncalled = pd.to_numeric(dataframe["uncalled_capital_usd"], errors="coerce")

    if (called > committed).any():
        issues.append(
            _issue(
                table_name="funds",
                check_name="called_capital_not_above_committed",
                message="Called capital cannot exceed committed capital",
            )
        )

    if (uncalled > committed).any():
        issues.append(
            _issue(
                table_name="funds",
                check_name="uncalled_capital_not_above_committed",
                message="Uncalled capital cannot exceed committed capital",
            )
        )

    return issues


def _check_commitment_math(raw_data_dir: Path) -> list[DataQualityIssue]:
    dataframe = _read_csv(raw_data_dir, "capital_commitments")
    issues = []

    if dataframe is None:
        return issues

    required = {"commitment_amount_usd", "called_amount_usd", "uncalled_amount_usd"}

    if not required.issubset(dataframe.columns):
        return issues

    commitment = pd.to_numeric(dataframe["commitment_amount_usd"], errors="coerce")
    called = pd.to_numeric(dataframe["called_amount_usd"], errors="coerce")
    uncalled = pd.to_numeric(dataframe["uncalled_amount_usd"], errors="coerce")

    if (commitment <= 0).any():
        issues.append(
            _issue(
                table_name="capital_commitments",
                check_name="commitment_positive",
                message="Investor commitments must be positive",
            )
        )

    if (called > commitment).any():
        issues.append(
            _issue(
                table_name="capital_commitments",
                check_name="called_not_above_commitment",
                message="Called amount cannot exceed investor commitment",
            )
        )

    if (uncalled > commitment).any():
        issues.append(
            _issue(
                table_name="capital_commitments",
                check_name="uncalled_not_above_commitment",
                message="Uncalled amount cannot exceed investor commitment",
            )
        )

    return issues


def _check_capital_call_dates_and_amounts(raw_data_dir: Path) -> list[DataQualityIssue]:
    dataframe = _read_csv(raw_data_dir, "capital_calls")
    issues = []

    if dataframe is None:
        return issues

    required = {"call_date", "due_date", "amount_called_usd", "amount_funded_usd"}

    if not required.issubset(dataframe.columns):
        return issues

    call_dates = pd.to_datetime(dataframe["call_date"], errors="coerce")
    due_dates = pd.to_datetime(dataframe["due_date"], errors="coerce")

    if (due_dates < call_dates).any():
        issues.append(
            _issue(
                table_name="capital_calls",
                check_name="due_date_after_call_date",
                message="Capital call due date must be on or after call date",
            )
        )

    amount_called = pd.to_numeric(dataframe["amount_called_usd"], errors="coerce")
    amount_funded = pd.to_numeric(dataframe["amount_funded_usd"], errors="coerce")

    if (amount_funded > amount_called).any():
        issues.append(
            _issue(
                table_name="capital_calls",
                check_name="funded_not_above_called",
                message="Funded amount cannot exceed called amount",
            )
        )

    return issues


def _check_facility_amounts(raw_data_dir: Path) -> list[DataQualityIssue]:
    dataframe = _read_csv(raw_data_dir, "facility_terms")
    issues = []

    if dataframe is None:
        return issues

    required = {"commitment_amount_usd", "outstanding_amount_usd"}

    if not required.issubset(dataframe.columns):
        return issues

    commitment = pd.to_numeric(dataframe["commitment_amount_usd"], errors="coerce")
    outstanding = pd.to_numeric(dataframe["outstanding_amount_usd"], errors="coerce")

    if (commitment <= 0).any():
        issues.append(
            _issue(
                table_name="facility_terms",
                check_name="facility_commitment_positive",
                message="Facility commitment must be positive",
            )
        )

    if (outstanding > commitment).any():
        issues.append(
            _issue(
                table_name="facility_terms",
                check_name="outstanding_not_above_commitment",
                message="Outstanding amount cannot exceed facility commitment",
            )
        )

    return issues


def _check_referential_integrity(raw_data_dir: Path) -> list[DataQualityIssue]:
    issues = []

    datasets: dict[str, pd.DataFrame] = {}

    for table_name in REQUIRED_FILES:
        dataframe = _read_csv(raw_data_dir, table_name)
        if dataframe is not None:
            datasets[table_name] = dataframe

    relationships = [
        ("funds", "manager_id", "fund_managers", "manager_id"),
        ("capital_commitments", "fund_id", "funds", "fund_id"),
        ("capital_commitments", "investor_id", "investors", "investor_id"),
        ("capital_calls", "fund_id", "funds", "fund_id"),
        ("capital_calls", "investor_id", "investors", "investor_id"),
        ("nav_history", "fund_id", "funds", "fund_id"),
        ("portfolio_companies", "fund_id", "funds", "fund_id"),
        ("facility_terms", "fund_id", "funds", "fund_id"),
        ("covenant_terms", "facility_id", "facility_terms", "facility_id"),
        ("monitoring_events", "fund_id", "funds", "fund_id"),
        ("monitoring_events", "facility_id", "facility_terms", "facility_id"),
    ]

    for child_table, child_key, parent_table, parent_key in relationships:
        if child_table not in datasets or parent_table not in datasets:
            continue

        child_dataframe = datasets[child_table]
        parent_dataframe = datasets[parent_table]

        if child_key not in child_dataframe.columns or parent_key not in parent_dataframe.columns:
            continue

        child_values = set(child_dataframe[child_key].dropna().astype(str))
        parent_values = set(parent_dataframe[parent_key].dropna().astype(str))

        orphan_values = sorted(child_values - parent_values)

        if orphan_values:
            sample_values = ", ".join(orphan_values[:5])
            issues.append(
                _issue(
                    table_name=child_table,
                    check_name="referential_integrity",
                    message=(
                        f"{child_key} contains values not found in "
                        f"{parent_table}.{parent_key}: {sample_values}"
                    ),
                )
            )

    return issues


def validate_raw_data(raw_data_dir: Path = RAW_DATA_DIR) -> list[DataQualityIssue]:
    issues = []
    issues.extend(_check_required_files_and_columns(raw_data_dir))
    issues.extend(_check_primary_keys(raw_data_dir))
    issues.extend(_check_fund_capital_math(raw_data_dir))
    issues.extend(_check_commitment_math(raw_data_dir))
    issues.extend(_check_capital_call_dates_and_amounts(raw_data_dir))
    issues.extend(_check_facility_amounts(raw_data_dir))
    issues.extend(_check_referential_integrity(raw_data_dir))
    return issues
