"""
data_prep.py — small reusable helpers for Project 2.

The notebooks explain the analysis slowly. This file keeps the repeat code in one
place so later notebooks can load the same clean data without copying everything.

Expected local data options:
    Option A (recommended): data/Online_Retail.xlsx
    Option B: data/Online_Retail.csv
    Option C (older split files):
        data/dataset_part_1.csv
        data/dataset_part_2.csv
        data/dataset_part_3_cleaned.csv

The data/ folder is ignored by git, so raw data is not uploaded to GitHub.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = "data"

RAW_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]

CANONICAL_COLUMNS = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_datetime",
    "unit_price",
    "customer_id",
    "country",
    "line_total",
]


def _standardize_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Rename the raw Online Retail columns into simple lower-case names."""
    out = pd.DataFrame({
        "invoice_no": df["InvoiceNo"].astype(str).str.strip(),
        "stock_code": df["StockCode"].astype(str).str.strip(),
        "description": df["Description"],
        "quantity": pd.to_numeric(df["Quantity"], errors="coerce"),
        "invoice_datetime": pd.to_datetime(df["InvoiceDate"], errors="coerce"),
        "unit_price": pd.to_numeric(df["UnitPrice"], errors="coerce"),
        "customer_id": df["CustomerID"].astype(str).str.replace(".0", "", regex=False).str.strip(),
        "country": df["Country"],
    })
    out["line_total"] = (out["quantity"] * out["unit_price"]).round(2)
    return out


def _standardize_part3(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize the older pre-cleaned part 3 file, if that file is used."""
    out = pd.DataFrame({
        "invoice_no": df["invoice_no"].astype(str).str.strip(),
        "stock_code": df["stock_code"].astype(str).str.strip(),
        "description": df["description"],
        "quantity": pd.to_numeric(df["quantity"], errors="coerce"),
        "invoice_datetime": pd.to_datetime(df["invoice_datetime"], errors="coerce"),
        "unit_price": pd.to_numeric(df["unit_price"], errors="coerce"),
        "customer_id": df["customer_id"].astype(str).str.replace(".0", "", regex=False).str.strip(),
        "country": df["country"],
        "line_total": pd.to_numeric(df["line_total"], errors="coerce"),
    })
    return out


def load_combined_dataset(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load the raw transaction data and return one standard table.

    The project first used three split files. To make the final repository easier
    to run, this function also accepts the original UCI/Kaggle Online Retail file.
    """
    data_path = Path(data_dir)
    xlsx_path = data_path / "Online_Retail.xlsx"
    csv_path = data_path / "Online_Retail.csv"
    part1_path = data_path / "dataset_part_1.csv"
    part2_path = data_path / "dataset_part_2.csv"
    part3_path = data_path / "dataset_part_3_cleaned.csv"

    if xlsx_path.exists():
        raw = pd.read_excel(xlsx_path, dtype={"CustomerID": str})
        combined = _standardize_raw(raw)
    elif csv_path.exists():
        raw = pd.read_csv(csv_path, dtype=str)
        combined = _standardize_raw(raw)
    elif part1_path.exists() and part2_path.exists() and part3_path.exists():
        d1 = pd.read_csv(part1_path, dtype=str)
        d2 = pd.read_csv(part2_path, dtype=str)
        d3 = pd.read_csv(part3_path, dtype=str)

        raw = pd.concat([_standardize_raw(d1), _standardize_raw(d2)], ignore_index=True)
        part3 = _standardize_part3(d3)

        # Some old split files overlap at the exact seam. Keep raw rows before part 3 starts.
        part3_start = part3["invoice_datetime"].min()
        raw_keep = raw[raw["invoice_datetime"] < part3_start].copy()
        combined = pd.concat([raw_keep, part3], ignore_index=True)
    else:
        raise FileNotFoundError(
            "No dataset found. Put Online_Retail.xlsx (or Online_Retail.csv) inside the data/ folder."
        )

    combined["customer_id"] = combined["customer_id"].replace({"nan": np.nan, "": np.nan, "None": np.nan})
    combined["description"] = combined["description"].replace({"nan": np.nan, "": np.nan})
    return combined.reset_index(drop=True)


def clean_dataset(combined: pd.DataFrame) -> pd.DataFrame:
    """Apply the Week 1 cleaning rules and return real purchase rows only."""
    work = combined.drop_duplicates()
    work = work[~work["invoice_no"].str.startswith("C", na=False)]
    work = work[work["quantity"] > 0]
    work = work[work["unit_price"] > 0]
    work = work[work["customer_id"].notna()]
    work = work.copy()
    work["line_total"] = (work["quantity"] * work["unit_price"]).round(2)
    return work.reset_index(drop=True)


def load_clean_dataset(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load + clean the data in one call."""
    return clean_dataset(load_combined_dataset(data_dir))


def add_cohort_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add transaction_month, cohort_month, and cohort_index columns."""
    out = df.copy()
    out["transaction_month"] = out["invoice_datetime"].dt.to_period("M")
    out["cohort_month"] = out.groupby("customer_id")["transaction_month"].transform("min")
    out["cohort_index"] = (
        (out["transaction_month"].dt.year - out["cohort_month"].dt.year) * 12
        + (out["transaction_month"].dt.month - out["cohort_month"].dt.month)
    )
    return out


def load_cohort_dataset(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load + clean + add cohort columns in one call."""
    return add_cohort_columns(load_clean_dataset(data_dir))


def build_cohort_count_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Count unique active customers for each cohort month and cohort index."""
    grouped = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique()
    cohort_counts = grouped.reset_index()

    matrix = cohort_counts.pivot_table(
        index="cohort_month",
        columns="cohort_index",
        values="customer_id",
    )
    return matrix


def build_retention_matrix(cohort_matrix: pd.DataFrame) -> pd.DataFrame:
    """Convert the cohort count matrix into retention rates from 0 to 1."""
    cohort_sizes = cohort_matrix.iloc[:, 0]
    retention = cohort_matrix.divide(cohort_sizes, axis=0)
    return retention


def add_customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create simple beginner-friendly customer value segments."""
    customer_revenue = df.groupby("customer_id")["line_total"].sum().rename("customer_revenue")
    customers = customer_revenue.reset_index()

    low_cut = customers["customer_revenue"].quantile(0.50)
    high_cut = customers["customer_revenue"].quantile(0.80)

    def segment_customer(revenue: float) -> str:
        if revenue >= high_cut:
            return "High value"
        if revenue >= low_cut:
            return "Medium value"
        return "Low value"

    customers["value_segment"] = customers["customer_revenue"].apply(segment_customer)
    out = df.merge(customers[["customer_id", "value_segment"]], on="customer_id", how="left")
    return out


if __name__ == "__main__":
    df = load_cohort_dataset()
    print("Clean rows       :", f"{len(df):,}")
    print("Unique customers :", f"{df['customer_id'].nunique():,}")
    print("Date range       :", df["invoice_datetime"].min(), "->", df["invoice_datetime"].max())
    print("Total revenue    : £", f"{df['line_total'].sum():,.2f}")
    print("Cohort index     :", df["cohort_index"].min(), "->", df["cohort_index"].max())
