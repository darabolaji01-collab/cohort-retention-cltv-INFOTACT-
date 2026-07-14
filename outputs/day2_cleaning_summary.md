# Day 2 — Data Cleaning Summary

**Milestone:** Week 1 data cleaning completed.

## What was built

- `notebooks/01_data_cleaning_eda.ipynb` — beginner-friendly cleaning notebook.
- `src/data_prep.py` — reusable helper functions so later notebooks can load the clean data easily.
- `outputs/cleaning_audit.csv` — row counts after each cleaning step.

## Cleaning rules used

1. Drop exact duplicate rows.
2. Remove cancelled invoices where `invoice_no` starts with `C`.
3. Keep only rows where `quantity > 0`.
4. Keep only rows where `unit_price > 0`.
5. Keep only rows with a valid `customer_id`.
6. Recalculate `line_total = quantity × unit_price`.

## Cleaning audit trail

| Step | Rows remaining | Rows removed |
|---|---:|---:|
| 0. Combined start | 541,909 | — |
| 1. Drop duplicate rows | 536,641 | 5,268 |
| 2. Remove cancelled invoices | 527,390 | 9,251 |
| 3. Keep quantity > 0 | 526,054 | 1,336 |
| 4. Keep unit_price > 0 | 524,878 | 1,176 |
| 5. Require customer_id present | **392,692** | 132,186 |

## Final cleaned dataset

| Metric | Value |
|---|---:|
| Rows | **392,692** |
| Unique customers | **4,338** |
| Unique invoices/orders | **18,532** |
| Date range | **2010-12-01 → 2011-12-09** |
| Countries | **37** |
| Total revenue | **£8,887,208.89** |

## Decision made

Rows with missing `customer_id` were removed because this project is about tracking customers over time. Without a customer ID, a row cannot be assigned to a cohort or used for retention.

## Next step

Add `transaction_month`, `cohort_month`, and `cohort_index` for every valid purchase row.
