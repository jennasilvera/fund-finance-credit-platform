#!/usr/bin/env bash
set -euo pipefail

echo "Running Fund Finance Credit Platform preflight checks..."
echo

echo "1. Checking Python linting..."
ruff check src tests

echo
echo "2. Running automated tests..."
pytest

echo
echo "3. Checking demo workflow shell syntax..."
bash -n scripts/demo_workflow.sh

echo
echo "4. Checking PostgreSQL connectivity..."
fund-finance check-db

echo
echo "5. Regenerating simulated raw data..."
python -m fund_finance.etl.generate_sample_data

echo
echo "6. Validating raw data quality..."
fund-finance validate-data

echo
echo "Preflight checks passed."
