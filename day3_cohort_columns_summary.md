# Day 3 — Cohort Month & Cohort Index Summary

**Milestone:** Week 1 continued — the cleaned data now has the columns needed for cohort analysis.

## What was built
- `notebooks/02_cohort_month_index.ipynb` — creates and verifies the cohort columns.
- `src/data_prep.py` — added `add_cohort_columns()` and `load_cohort_dataset()` so any later
  notebook gets the cohort-ready table in one line.

## New columns added to every row

| Column | Meaning | Example |
|---|---|---|
| `transaction_month` | Month the purchase happened | `2011-03` |
| `cohort_month` | The customer's **first** purchase month (their group) | `2010-12` |
| `cohort_index` | Whole months since first purchase (0 = first month) | `3` |

## Verification (all checks passed)
- Rows with a negative `cohort_index`: **0** (no purchase happens before a customer's first purchase).
- Missing values in the new columns: **0**.
- `cohort_index` range: **0 → 12** (matches the 13-month window Dec 2010 → Dec 2011).
- Sum of cohort sizes = **4,338** = total unique customers ✅
- Manual spot-check on repeat customer `15311`: first bought Dec 2010 (index 0), then returned
  every following month (index 1, 2, 3, …) — exactly as expected.

## Cohort sizes (new customers per first-purchase month)

| Cohort month | New customers |
|---|---:|
| 2010-12 | **885** (largest) |
| 2011-01 | 417 |
| 2011-02 | 380 |
| 2011-03 | 452 |
| 2011-04 | 300 |
| 2011-05 | 284 |
| 2011-06 | 242 |
| 2011-07 | 188 |
| 2011-08 | 169 |
| 2011-09 | 299 |
| 2011-10 | 358 |
| 2011-11 | 323 |
| 2011-12 | 41 |

*(The Dec 2010 cohort is largest because it captures everyone already active when records began.)*

## Files saved
- `data/cleaned_with_cohorts.csv` — enriched table for Week 2 (**local only, git-ignored**).

## Next step (start of Week 2)
Build the **retention count matrix** with `pivot_table` (rows = `cohort_month`, columns =
`cohort_index`), then divide each row by its Month-0 size to get the **retention percentage
matrix** — the data behind the heatmap.
