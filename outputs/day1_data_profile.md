# Day 1 — Initial Data Profile

Quick, factual snapshot of the dataset created on **Day 1** so future work has a
reliable reference. This is a *profile only* — no cleaning or analysis has been done yet.

## Files received

| File | Role | Columns | Rows (data) | Date range |
|---|---|---|---|---|
| `dataset_part_1.csv` | Raw slice #1 | 8 | ~180,637 | 2010-12-01 → 2011-09-26 |
| `dataset_part_2.csv` | Raw slice #2 | 8 | ~180,636 | 2011-05 → 2011-09-26 |
| `dataset_part_3_cleaned.csv` | Pre-cleaned slice #3 | 13 (enriched) | ~178,174 | 2011-09-26 → 2011-12-09 |

**Interpretation:** The three files are **chronological pieces of ONE dataset** — the
well-known *Online Retail* dataset (UK online gift retailer). Parts 1–2 are raw
(original 8 columns). Part 3 covers the final months and already includes helpful
cleaning columns (`line_total`, `invoice_status`, `line_type`, `data_quality_flags`).
Combined, they cover a continuous **~13-month timeline** — ideal for cohort analysis.

## Combined whole-timeline profile (all three parts)

| Metric | Value |
|---|---|
| Total line-item rows | **539,447** |
| Date range | **2010-12-01 → 2011-12-09** (~13 months) |
| Unique invoices | 25,900 |
| Unique customers | 4,372 |
| Countries | 38 |
| Rows missing `CustomerID` | **135,072 (≈25.0%)** → must be handled |
| Cancellation invoices (`InvoiceNo` starts with `C`) | 9,274 → must be filtered |
| Negative-quantity rows (returns) | 10,610 → must be filtered |
| Exact duplicate rows | 2,806 → must be removed |
| Rows missing `Description` | 1,454 |

## Data-quality issues to fix in Week 1 (cleaning)

1. **Missing `CustomerID` (~25%)** — cohort analysis needs a customer to track, so
   rows without an ID cannot be used for retention. Decide: drop for cohort work.
2. **Cancellations / returns** — `InvoiceNo` values starting with `C` and negative
   `Quantity` are refunds/returns; remove them from purchase-based cohorts.
3. **Duplicate rows** — remove exact duplicates.
4. **Date parsing** — raw dates are `M/D/YYYY H:MM`; part 3 dates are ISO
   `YYYY-MM-DD HH:MM:SS`. Both must be parsed to a single datetime format.
5. **Revenue column** — raw data has no total; compute `line_total = Quantity × UnitPrice`
   (part 3 already provides `line_total`).
6. **Zero / negative prices** — present in part 3's quality flags; review and filter.

## Notes for the next step (Week 1 cleaning notebook)

- Standardize both schemas into one table with columns:
  `invoice_no, stock_code, description, quantity, invoice_datetime, unit_price,
  customer_id, country, line_total`.
- Keep raw files in the local `data/` folder (git-ignored).
