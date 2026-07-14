# SaaS / E-Commerce Cohort Retention & CLTV Analysis

**Infotact Technical Internship — Data Analytics Project 2**

This project studies customer retention and Customer Lifetime Value (CLTV) using the Online Retail transaction dataset. I grouped customers by the month they first purchased, measured how many returned in later months, then calculated simple historical CLTV and customer value segments.

---

## Business problem

Acquiring new customers is expensive, but a business only becomes healthy if customers keep coming back. This project answers two main questions:

1. **Retention:** After a customer's first purchase, do they return in Month 1, Month 2, and later months?
2. **CLTV:** How much revenue does an average customer generate, and which customer segments are most valuable?

The final goal is to help a product or finance team understand churn patterns and make better retention decisions.

---

## Dataset

**Dataset:** Online Retail dataset (UCI Machine Learning Repository / Kaggle)

**Period covered:** 01 Dec 2010 to 09 Dec 2011

**Main columns used:**

- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

> Raw data is **not stored in this repository**. The `data/` folder is ignored by git so that raw CSV/XLSX files are not uploaded.

### How to get the data

Download the Online Retail dataset and place it here:

```text
data/Online_Retail.xlsx
```

The helper code also supports `data/Online_Retail.csv` if you use a CSV version.

---

## Folder structure

```text
.
├── .github/workflows/             # GitHub Actions workflow
├── data/                          # Local raw data only (ignored by git)
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   ├── 02_cohort_month_index.ipynb
│   ├── 03_cohort_retention_matrix.ipynb
│   ├── 04_cltv_analysis.ipynb
│   └── 05_visualizations_insights.ipynb
├── outputs/
│   ├── cohort_retention_heatmap.png
│   ├── retention_curves.png
│   ├── cohort_cltv_bar_chart.png
│   ├── segment_revenue_share.png
│   ├── top_countries_revenue.png
│   └── summary CSV/Markdown files
├── reports/
│   └── final_business_summary.md
├── src/
│   └── data_prep.py
├── tests/
│   └── test_data_prep.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Technologies used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Pytest
- Git and GitHub

---

## Setup instructions

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Run the notebooks in this order:

1. `notebooks/01_data_cleaning_eda.ipynb`
2. `notebooks/02_cohort_month_index.ipynb`
3. `notebooks/03_cohort_retention_matrix.ipynb`
4. `notebooks/04_cltv_analysis.ipynb`
5. `notebooks/05_visualizations_insights.ipynb`

You can also run a quick code check with:

```bash
pytest
```

---

## Analysis workflow

### Week 1 — Data cleaning and cohort setup

- Loaded the transaction dataset.
- Standardized column names.
- Removed duplicate rows.
- Removed cancellations/refunds.
- Removed non-positive quantities and prices.
- Removed rows without customer IDs for cohort analysis.
- Added:
  - `transaction_month`
  - `cohort_month`
  - `cohort_index`

### Week 2 — Cohort retention matrix

- Built a cohort count matrix.
- Built a retention percentage matrix.
- Validated that Month 0 retention is 100% for every cohort.
- Saved the retention matrices to `outputs/`.

### Week 3 — CLTV analysis

- Calculated total revenue.
- Calculated Average Order Value (AOV).
- Calculated purchase frequency.
- Calculated historical CLTV.
- Segmented customers into low, medium, and high value groups.
- Compared CLTV by country and cohort.

### Week 4 — Visualizations and insights

- Created cohort retention heatmap.
- Created retention curves.
- Created CLTV and customer segment charts.
- Wrote final business recommendations.

---

## Key findings

After cleaning, the analysis dataset contained:

| Metric | Value |
|---|---:|
| Clean rows | 392,692 |
| Unique customers | 4,338 |
| Unique orders | 18,532 |
| Countries | 37 |
| Total revenue | £8,887,208.89 |

Retention findings:

| Metric | Value |
|---|---:|
| Average Month 1 retention | 20.6% |
| Average Month 2 retention | 22.1% |
| Main issue | Large drop after first purchase |

CLTV findings:

| Metric | Value |
|---|---:|
| Average Order Value | £479.56 |
| Purchase Frequency | 4.27 orders per customer |
| Historical CLTV | £2,048.69 per customer |

Customer segment findings:

| Segment | Customers | Revenue share | Historical CLTV |
|---|---:|---:|---:|
| High value | 868 | 74.7% | £7,646.66 |
| Medium value | 1,301 | 17.5% | £1,196.03 |
| Low value | 2,169 | 7.8% | £319.90 |

---

## Visualizations

The final charts are saved in the `outputs/` folder:

- `outputs/cohort_retention_heatmap.png`
- `outputs/retention_curves.png`
- `outputs/cohort_cltv_bar_chart.png`
- `outputs/segment_revenue_share.png`
- `outputs/top_countries_revenue.png`

---

## Business recommendations

1. **Improve early retention.** Since Month 1 retention is low, the business should send a follow-up email, discount, or product recommendation within the first few weeks after the first purchase.
2. **Protect high-value customers.** The top 20% of customers generate most of the revenue, so they should receive better retention attention.
3. **Move medium-value customers upward.** Medium-value customers already buy more than low-value customers, so targeted offers may encourage them to repeat purchase.
4. **Use CLTV for acquisition decisions.** The business should avoid spending more on customer acquisition than a segment is likely to return.
5. **Track cohorts every month.** Retention should be monitored regularly, not only once.

---

## Future improvements

- Add marketing channel data to compare retention by acquisition source.
- Analyze product categories bought by high-value customers.
- Build a simple predictive 12-month CLTV model when more data is available.
- Create a dashboard in Power BI, Tableau, or Streamlit.

---

## Project status

All required deliverables for **Project 2: SaaS / E-Commerce Cohort Retention & CLTV Analysis** have been completed:

- Week 1 cleaning and cohort setup ✅
- Week 2 retention matrix ✅
- Week 3 CLTV analysis ✅
- Week 4 visualizations and business insights ✅
