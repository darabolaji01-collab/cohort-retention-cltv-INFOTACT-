# SaaS / E-Commerce Cohort Retention & CLTV Analysis

**Infotact Technical Internship — Data Analytics Project 2**

> **Project in one sentence:** Group customers by the month they first purchased,
> measure how many keep coming back over time, calculate how much they are worth
> (Customer Lifetime Value), and recommend ways to reduce churn and improve profitability.

---

## 1. Business Problem

Acquiring a new customer can cost up to **5× more** than keeping an existing one.
Many companies celebrate fast user growth but never check whether those users *stay*.
If a business loses customers faster than it wins them, it will eventually collapse.

This project answers two questions with data:

1. **Retention** — After a customer's first purchase, do they come back? *When* do they leave?
2. **CLTV (Customer Lifetime Value)** — How much revenue is a customer worth over their lifetime,
   and how does that differ between customer segments?

## 2. Who Uses This Analysis

| Persona | What they need | How they use this work |
|---|---|---|
| **Product Manager** | Understand user stickiness & drop-off | Reads the retention heatmap to find the month where churn is highest, then plans product fixes / re-engagement. |
| **Finance Director** | Revenue forecasting & profitability | Uses CLTV to decide the maximum Customer Acquisition Cost (CAC) the business can afford while staying profitable. |

## 3. Dataset

**Source:** *Online Retail* dataset — real transactions from a UK-based online gift retailer,
covering **01 Dec 2010 → 09 Dec 2011** (~13 months). Publicly available from the
UCI Machine Learning Repository / Kaggle ("Online Retail").

> ⚠️ **Data is NOT stored in this repository.** Per Infotact rules, raw data files are
> excluded via `.gitignore`. To run the analysis, place the data files inside a local
> `data/` folder (see *How to Run* below).

**Columns (raw):** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`,
`UnitPrice`, `CustomerID`, `Country`.

**Key facts observed during initial profiling (Day 1):**

| Metric | Value |
|---|---|
| Total line-item rows | ~539,000 |
| Date range | 2010-12-01 → 2011-12-09 (~13 months) |
| Unique customers | ~4,370 |
| Countries | 37+ |
| Rows missing `CustomerID` | large share — must be handled in cleaning |
| Cancellation invoices (InvoiceNo starts with `C`) | present — must be filtered |
| Negative quantities (returns) | present — must be filtered |
| Duplicate rows | present — must be removed |

*(Exact numbers are recorded in `outputs/day1_data_profile.md`.)*

## 4. Planned Deliverables

- **Code:** Jupyter notebooks + `requirements.txt` + clean folder structure
- **Analysis:** cleaned data process, cohort-month calculation, retention count matrix,
  retention percentage heatmap, CLTV by segment
- **Presentation:** this README, charts/screenshots, business insights & recommendations
- **Process:** GitHub commit history spread across all 4 weeks (mandatory for evaluation)

## 5. Repository Structure

```
.
├── README.md              # This file — project overview
├── .gitignore             # Keeps raw data & secrets out of GitHub
├── requirements.txt       # Python packages needed
├── data/                  # (LOCAL ONLY — ignored by git) put dataset files here
├── notebooks/             # Jupyter notebooks for each analysis step
├── src/                   # Reusable Python helper scripts
├── outputs/               # Generated charts, tables, profile reports
└── reports/               # Written summaries & business recommendations
```

## 6. Formulas Used (reference)

| Metric | Formula |
|---|---|
| Retention Rate | active users in later month ÷ original cohort size × 100 |
| Churn Rate | 100% − Retention Rate |
| Average Order Value (AOV) | Total Revenue ÷ Number of Orders |
| Purchase Frequency | Number of Orders ÷ Number of Unique Customers |
| Customer Value | AOV × Purchase Frequency |
| Simple CLTV | AOV × Purchase Frequency × Customer Lifespan |

## 7. How to Run (once data is added)

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Put the dataset files inside a local  data/  folder
#    (this folder is git-ignored and will NOT upload)

# 3. Launch Jupyter and open the notebooks in order
jupyter notebook
```

## 8. Tools

Python · Pandas · NumPy · Matplotlib · Seaborn · Jupyter Notebook · Git · GitHub.

## 9. Progress Log

| Week | Focus | Status |
|---|---|---|
| Week 1 | Data cleaning & EDA | 🟡 In progress (Day 1: setup + profiling · Day 2: combined 3 files + cleaned → 392,687 rows) |
| Week 2 | Cohort retention matrix | ⬜ Not started |
| Week 3 | CLTV calculation | ⬜ Not started |
| Week 4 | Visualization & insights | ⬜ Not started |

## 10. Assumptions & Limitations

- The three uploaded dataset parts are **chronological slices** of one dataset
  (Parts 1–2 = Dec 2010→Sep 2011 raw; Part 3 = Sep→Dec 2011, pre-cleaned) and will be
  combined into one continuous timeline during Week 1.
- Refunds, cancellations, missing customer IDs, and duplicate rows will be removed before
  cohort analysis, following the project specification.

---

*Author: Data Analytics Intern — Infotact Program.*
