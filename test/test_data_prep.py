import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.data_prep import (  # noqa: E402
    add_cohort_columns,
    build_cohort_count_matrix,
    build_retention_matrix,
    clean_dataset,
)


def make_sample_transactions():
    return pd.DataFrame({
        "invoice_no": ["100", "101", "C102", "103", "104", "105"],
        "stock_code": ["A", "B", "C", "D", "E", "F"],
        "description": ["item", "item", "return", "bad qty", "bad price", "missing customer"],
        "quantity": [1, 2, -1, 0, 1, 1],
        "invoice_datetime": pd.to_datetime([
            "2021-01-10", "2021-02-10", "2021-02-11", "2021-03-01", "2021-03-02", "2021-03-03"
        ]),
        "unit_price": [10.0, 5.0, 5.0, 7.0, 0.0, 3.0],
        "customer_id": ["1", "1", "1", "2", "2", None],
        "country": ["UK", "UK", "UK", "UK", "UK", "UK"],
        "line_total": [10.0, 10.0, -5.0, 0.0, 0.0, 3.0],
    })


def test_clean_dataset_keeps_only_valid_customer_purchases():
    sample = make_sample_transactions()
    clean = clean_dataset(sample)

    assert len(clean) == 2
    assert clean["invoice_no"].tolist() == ["100", "101"]
    assert clean["line_total"].sum() == 20.0


def test_cohort_columns_and_retention_matrix():
    sample = make_sample_transactions()
    clean = clean_dataset(sample)
    cohort_df = add_cohort_columns(clean)

    assert cohort_df["cohort_month"].astype(str).unique().tolist() == ["2021-01"]
    assert cohort_df["cohort_index"].tolist() == [0, 1]

    cohort_matrix = build_cohort_count_matrix(cohort_df)
    retention = build_retention_matrix(cohort_matrix)

    assert cohort_matrix.loc[pd.Period("2021-01", freq="M"), 0] == 1
    assert retention.loc[pd.Period("2021-01", freq="M"), 1] == 1.0
