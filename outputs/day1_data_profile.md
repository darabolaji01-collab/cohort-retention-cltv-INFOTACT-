# Day 1 — Initial Data Profile

Quick snapshot of the raw Online Retail transaction dataset before cleaning.

## Dataset used

**Online Retail** dataset from the UCI Machine Learning Repository / Kaggle.
It contains transactions for a UK-based online retailer from **2010-12-01 to 2011-12-09**.
The raw data is kept locally in the `data/` folder and is not pushed to GitHub.

## Raw dataset profile

| Metric | Value |
|---|---:|
| Total line-item rows | **541,909** |
| Date range | **2010-12-01 → 2011-12-09** |
| Unique invoices | **25,900** |
| Unique customers before cleaning | **4,372** |
| Countries | **38** |
| Rows missing `CustomerID` | **135,080** (~24.9%) |
| Cancellation invoices (`InvoiceNo` starts with `C`) | **9,288** |
| Negative-quantity rows | **10,624** |
| Exact duplicate rows | **5,268** |
| Rows missing `Description` | **1,454** |

## Data-quality issues found

1. **Missing customer IDs** — cohort retention cannot track an unknown customer, so these rows must be removed for the main analysis.
2. **Cancellations and refunds** — invoices starting with `C` and negative quantities are not normal purchases.
3. **Duplicate rows** — exact repeats would inflate revenue and purchase counts.
4. **Date parsing** — `InvoiceDate` must be converted from text into a real datetime column.
5. **Revenue column** — the raw file does not directly give line revenue, so `line_total = Quantity × UnitPrice` is calculated.
6. **Zero or negative prices** — these are not useful for purchase-based CLTV.

## Next step

Clean the data step-by-step, record the number of rows removed at each step, and create the columns needed for cohort analysis.
