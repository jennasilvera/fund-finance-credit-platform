#!/usr/bin/env bash
set -euo pipefail

echo "Starting Fund Finance Credit Platform demo workflow..."
echo

echo "1. Generating simulated raw data..."
python -m fund_finance.etl.generate_sample_data

echo
echo "2. Running raw data quality validation..."
fund-finance validate-data

echo
echo "3. Loading data into PostgreSQL..."
fund-finance load-data

echo
echo "4. Checking table row counts..."
fund-finance row-counts

echo
echo "5. Running subscription borrowing base analysis for FAC001..."
fund-finance run-subscription-borrowing-base --facility-id FAC001

echo
echo "6. Running hybrid NAV analysis for FAC002..."
fund-finance run-nav-borrowing-base --facility-id FAC002

echo
echo "7. Running NAV analysis for FAC003..."
fund-finance run-nav-borrowing-base --facility-id FAC003

echo
echo "8. Running covenant monitoring for all facilities..."
fund-finance run-covenant-monitoring --facility-id ALL

echo
echo "9. Running credit scoring for all facilities..."
fund-finance run-credit-scoring --facility-id ALL

echo
echo "10. Generating credit memo for breached hybrid facility FAC002..."
fund-finance generate-credit-memo --facility-id FAC002

echo
echo "Demo workflow complete."
echo "Generated credit memos can be found in data/outputs/credit_memos/"
