# Power BI Desktop implementation (a guide, not a claimed .pbix file)

## 1. Load tables
Open Power BI Desktop → Get Data → Text/CSV and load:
`data/commercial_sales.csv`, `data/products.csv`, `data/physicians.csv`, `data/synthetic_therapy_episodes.csv`.

If data CSVs are not present in your clone, first run `python -m src.generate_data`. They are generated deterministically.

## 2. Set relationships
- `products[product_id]` (one) → `commercial_sales[product_id]` (many).
- `products[product_id]` (one) → `synthetic_therapy_episodes[product_id]` (many).
- Keep `physicians` separate unless you create a unique `region × therapy_area` summary table; **do not** directly create an ambiguous many-to-many relationship between `physicians` and `commercial_sales`.
- For consistent regional filtering, create a one-row-per-region Region dimension and relate it to the three corresponding facts. Make a Date dimension for monthly time intelligence.

## 3. Measures in DAX
```DAX
Revenue = SUM(commercial_sales[revenue_inr])
COGS = SUM(commercial_sales[cogs_inr])
Gross Profit = [Revenue] - [COGS]
Gross Margin = DIVIDE([Gross Profit], [Revenue])
Promotion Spend = SUM(commercial_sales[promotion_spend_inr])
Contribution After Promotion = [Gross Profit] - [Promotion Spend]
Calls = SUM(commercial_sales[sales_calls])
Revenue per Call = DIVIDE([Revenue], [Calls])
Therapy Episodes = COUNTROWS(synthetic_therapy_episodes)
Discontinued Episodes = CALCULATE([Therapy Episodes], synthetic_therapy_episodes[day_120_status] = "discontinued")
Discontinuation Rate = DIVIDE([Discontinued Episodes], [Therapy Episodes])
```

## 4. Proposed report pages
1. Executive overview: revenue, gross profit, margin, contribution after promotion, monthly sales trend.
2. Regional/product economics: clustered bars, product margin matrix, region filters.
3. Physician-segment opportunity: synthetic potential and low-visit counts by region/therapy (without personal identification).
4. Aggregate therapy continuity: product/region synthetic discontinuation, clearly labeled as simulated.
5. Strategy priorities: import `outputs/segment_prioritization.csv`, show the score plus all four component measures and a note on weights/limitations.

## 5. Quality checks
- The Revenue and Gross Profit cards must match `outputs/executive_kpis.csv`.
- Use source grain and cardinality checks to avoid duplicated sales from many-to-many joins.
- Clearly label all report pages **Synthetic portfolio case — not clinical evidence**.
- Save your actual `.pbix` only after building these pages in Power BI Desktop.
