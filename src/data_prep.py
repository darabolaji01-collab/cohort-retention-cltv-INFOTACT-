"""
data_prep.py — reusable data-loading & cleaning helpers for Project 2.

Why this file exists:
    The notebook (notebooks/01_data_cleaning_eda.ipynb) explains the cleaning step by
    step for learning. This module packages that same logic into functions so later
    notebooks (Week 2, 3, 4) can get the clean data in ONE line instead of copying code.

Usage (from the repo root):
    from src.data_prep import load_clean_dataset
    df = load_clean_dataset()

Data location:
    Expects the three files inside a local  data/  folder (git-ignored):
        data/dataset_part_1.csv
        data/dataset_part_2.csv
        data/dataset_part_3_cleaned.csv
"""
from __future__ import annotations
import pandas as pd
import numpy as np

DATA_DIR = "data"

CANONICAL_COLS = [
    "invoice_no", "stock_code", "description", "quantity",
    "invoice_datetime", "unit_price", "customer_id", "country", "line_total",
]


def _standardize_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Rename the raw 8-column files into the canonical lower-case schema."""
    out = pd.DataFrame({
        "invoice_no":       df["InvoiceNo"].astype(str).str.strip(),
        "stock_code":       df["StockCode"].astype(str).str.strip(),
        "description":      df["Description"],
        "quantity":         pd.to_numeric(df["Quantity"], errors="coerce"),
        "invoice_datetime": pd.to_datetime(df["InvoiceDate"], errors="coerce"),
        "unit_price":       pd.to_numeric(df["UnitPrice"], errors="coerce"),
        "customer_id":      df["CustomerID"].astype(str).str.strip(),
        "country":          df["Country"],
    })
    out["line_total"] = (out["quantity"] * out["unit_price"]).round(2)
    out["source_file"] = "raw_parts_1_2"
    return out


def _standardize_part3(df: pd.DataFrame) -> pd.DataFrame:
    """Select the shared columns from the pre-cleaned file (part 3)."""
    out = pd.DataFrame({
        "invoice_no":       df["invoice_no"].astype(str).str.strip(),
        "stock_code":       df["stock_code"].astype(str).str.strip(),
        "description":      df["description"],
        "quantity":         pd.to_numeric(df["quantity"], errors="coerce"),
        "invoice_datetime": pd.to_datetime(df["invoice_datetime"], errors="coerce"),
        "unit_price":       pd.to_numeric(df["unit_price"], errors="coerce"),
        "customer_id":      df["customer_id"].astype(str).str.strip(),
        "country":          df["country"],
        "line_total":       pd.to_numeric(df["line_total"], errors="coerce"),
    })
    out["source_file"] = "cleaned_part_3"
    return out


def load_combined_dataset(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load all three parts and combine them into one continuous table.

    Handles the seam overlap: the raw files end on the same timestamp that the
    cleaned file (part 3) begins (invoice 568346 @ 2011-09-26 15:28:00). We keep
    raw rows only *before* part 3 starts so nothing is double-counted.
    """
    d1 = pd.read_csv(f"{data_dir}/dataset_part_1.csv", dtype=str)
    d2 = pd.read_csv(f"{data_dir}/dataset_part_2.csv", dtype=str)
    d3 = pd.read_csv(f"{data_dir}/dataset_part_3_cleaned.csv", dtype=str)

    raw = pd.concat([_standardize_raw(d1), _standardize_raw(d2)], ignore_index=True)
    part3 = _standardize_part3(d3)

    p3_start = part3["invoice_datetime"].min()
    raw_keep = raw[raw["invoice_datetime"] < p3_start].copy()

    combined = pd.concat([raw_keep, part3], ignore_index=True)
    combined["customer_id"] = combined["customer_id"].replace({"nan": np.nan, "": np.nan})
    combined["description"] = combined["description"].replace({"nan": np.nan})
    return combined


def clean_dataset(combined: pd.DataFrame) -> pd.DataFrame:
    """Apply the Week 1 cleaning rules and return a purchase-only table.

    Steps: drop duplicates -> remove cancellations -> keep quantity>0 ->
    keep unit_price>0 -> require a customer_id -> recompute line_total.
    """
    work = combined.drop_duplicates()
    work = work[~work["invoice_no"].str.startswith("C")]
    work = work[work["quantity"] > 0]
    work = work[work["unit_price"] > 0]
    work = work[work["customer_id"].notna()]
    work = work.copy()
    work["line_total"] = (work["quantity"] * work["unit_price"]).round(2)
    return work.reset_index(drop=True)


def load_clean_dataset(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Convenience: load + combine + clean in one call."""
    return clean_dataset(load_combined_dataset(data_dir))


if __name__ == "__main__":
    df = load_clean_dataset()
    print("Clean rows        :", f"{len(df):,}")
    print("Unique customers  :", f"{df['customer_id'].nunique():,}")
    print("Date range        :", df["invoice_datetime"].min(), "->", df["invoice_datetime"].max())
    print("Total revenue     : £", f"{df['line_total'].sum():,.2f}")
