# Day 2 — Data Combining & Cleaning Summary

**Milestone:** Week 1 begun — three dataset parts combined into one clean table.

## What was built
- `notebooks/01_data_cleaning_eda.ipynb` — step-by-step combining + cleaning notebook.
- `src/data_prep.py` — reusable functions (`load_clean_dataset()`) that reproduce the same result in one line.

## Combining the three files
The three files are chronological slices of one dataset. Raw parts (1 & 2) use capitalised
columns (`InvoiceNo`, `CustomerID`); the pre-cleaned part 3 uses lower-case names plus extra
columns. They were unified into one **canonical schema**:

`invoice_no, stock_code, description, quantity, invoice_datetime, unit_price, customer_id, country, line_total`

### ⚠️ Seam overlap fixed
The raw files **end** on the exact timestamp the cleaned file **begins**
(`2011-09-26 15:28:00`), and invoice **`568346`** appears in both. To avoid
double-counting, raw rows were kept only for dates **strictly before** part 3's start.
This removed **5** duplicated seam rows and produced a continuous, gap-free 13-month timeline.

## Cleaning audit trail (rows remaining after each step)

| Step | Rows remaining | Rows removed |
|---|---:|---:|
| 0. Combined (start) | 539,442 | — |
| 1. Drop duplicate rows | 536,636 | 2,806 |
| 2. Remove cancellation invoices (`C…`) | 527,385 | 9,251 |
| 3. Keep quantity > 0 | 526,049 | 1,336 |
| 4. Keep unit_price > 0 | 524,873 | 1,176 |
| 5. Require customer_id present | 392,687 | 132,186 |

## Final cleaned dataset

| Metric | Value |
|---|---|
| Rows | **392,687** |
| Unique customers | **4,338** |
| Unique invoices | 18,532 |
| Date range | 2010-12-01 → 2011-12-09 (13 continuous months) |
| Countries | 37 |
| Total revenue | **£8,887,169.13** |

## Decisions & assumptions
- Rows with a missing `customer_id` (~25%) are removed **for cohort/CLTV work** because
  retention must follow a known customer.
- `line_total` is recomputed as `quantity × unit_price` for consistency across all rows.

## Next step (Week 1 continues)
Add `transaction_month` and each customer's `cohort_month` (first purchase month) — the
foundation for the Week 2 retention matrix.
