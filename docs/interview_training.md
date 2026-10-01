# Healthcare strategy project | from fundamentals to interview defense

## A. Your problem statement
“A hypothetical healthcare commercial team wants to prioritize limited field resources across regions and fictional product lines without mistaking correlation for causation or commercial metrics for medical evidence.” Your goal is to **frame the business decision**, establish clean metrics, find descriptive gaps, develop a transparent scoring framework and recommend a measured pilot.

## B. Understand the four datasets
1. `products.csv`: six fictional product IDs, therapy area, list price and unit COGS. Grain = one row per product.
2. `physicians.csv`: 240 made-up physician IDs grouped into regions and therapy areas, with artificial potential and recent field visits. Grain = one fictional physician.
3. `commercial_sales.csv`: 288 records = 12 months × 4 regions × 6 products. It includes units, realized net price, revenue, COGS, promotion spending, calls and prescriptions. Grain = month–region–product.
4. `synthetic_therapy_episodes.csv`: 8,000 independent fake therapy episodes; each has a fictional ID, region/product, start cohort, 120-day status and simulated observed days. The file is **not** linked to an individual doctor or commercial transaction.

## C. Trace every line of the pipeline
- `src/generate_data.py` creates deterministic synthetic source CSVs with random seed `20261001`.
- `src/analyze.py` validates sales arithmetic and unique grain, merges products onto sales, aggregates region/product metrics, derives aggregate low-engagement physician potential and fake discontinuation rates, ranks the 24 region/product groups, writes charts and an executive memo.
- `src/build_sqlite.py` creates an actual SQLite database from the schema and populates it from the CSVs. `sql/02_analysis_queries.sql` is a query-practice sheet.
- `tests/test_strategy.py` verifies arithmetic, uniqueness, reproducibility, scoring bounds and status validity.

## D. Must-know calculations
- Revenue = units × net price. Example: 1,000 units × INR 850 = INR 850,000.
- COGS = units × unit cost. Example: 1,000 × INR 390 = INR 390,000.
- Gross profit = INR 850,000 − INR 390,000 = INR 460,000.
- Gross margin = 460,000/850,000 = **54.12%**.
- Contribution after promotion = gross profit − allocated promotion spend. With INR 70,000 promotion spend, the result is INR 390,000. This is **not** net income.
- Revenue per call = group revenue / commercial calls. It measures a ratio; it does not prove each call generated the revenue.
- Discontinuation rate = synthetic episodes labeled discontinued / all episodes in a group. It is a simulation, not measured clinical persistence.

## E. Priority scoring
For each of 24 region/product combinations, calculate percentile ranks for revenue, gross margin, synthetic under-engaged physician potential in the matching region/therapy, and simulated aggregate discontinuation. Then compute `100 × (0.30 × revenue percentile + 0.30 × margin percentile + 0.20 × potential percentile + 0.20 × discontinuation percentile)`.

**Interpretation:** The score creates a *transparent shortlist for investigation*, not a proven ROI, market opportunity or medical decision. A higher simulated discontinuation signal triggers a **medical/compliance review**, not treatment or patient-level targeting. Real companies would validate weights and separate commercial and medical workstreams.

## F. SQL questions you must answer
1. **How do you rank products by profit?** Aggregate gross profit by product in a CTE, then `DENSE_RANK() OVER(ORDER BY gross_profit DESC)`.
2. **How do you calculate monthly change?** `LAG(revenue) OVER(PARTITION BY region ORDER BY month)` then divide the difference by prior-month revenue using `NULLIF` to prevent division by zero.
3. **How do you find under-engaged physician segments?** Filter fictional `field_visits_last_quarter < 3`, then group and sum estimated potential by region and therapy area.
4. **How do you prevent double counting?** Preserve grain: one product per sales record, unique month/region/product keys, join against a one-row-per-product dimension. Do not join individual physicians directly onto sales by region alone.
5. **What is the difference between `ROW_NUMBER`, `RANK`, `DENSE_RANK`?** `ROW_NUMBER` always assigns unique sequential positions, `RANK` has gaps after ties, `DENSE_RANK` has no gaps.

## G. Consulting PI questions and reasoning
1. **What business decision does your model support?** It produces an evidence-organized shortlist of region/product combinations for *further testing* under resource constraints.
2. **Why use gross margin rather than revenue alone?** A high-revenue segment can destroy value when cost of sales is high.
3. **Why track contribution after promotion?** It adds commercial-spend context without falsely claiming to model every operating cost.
4. **Why create a scoring framework?** To surface assumptions, compare unlike signals transparently and discuss trade-offs with stakeholders.
5. **Why these specific weights?** Illustrative; they are not estimated causal coefficients or validated strategy weights. In real work I would run stakeholder workshops and sensitivity analysis.
6. **What does physician whitespace mean?** Artificial estimated Rx potential in an under-engaged region/therapy segment. It is a hypothesis for compliant channel review, not a promise of incremental prescriptions.
7. **What would an experiment measure?** Pre-defined changes in gross profit after promotion, aggregate engagement metrics and governed continuity measures against a comparison group.
8. **What is the main data limitation?** Every source is simulated; patient episodes are independently generated, observational measures are noncausal, and true market share is unknown.
9. **Does discontinuation mean a product is ineffective?** No. It can reflect tolerability, adherence support, affordability, disease course, data-generation rules or other factors, and needs medical evaluation.
10. **What might a consultant ask for next?** Real market/competitive data, regulatory constraints, verified field activity, product lifecycle, pricing/reimbursement and stakeholder objectives.
11. **Could you use the data for individual patient targeting?** No. There are no real patients, and clinical/privacy decisions require separate governance.
12. **Where is the project most like consulting?** Clear problem framing, defensible KPIs, prioritization, trade-off analysis, written recommendation and pilot evaluation.
13. **What did you personally build?** Synthetic generator, reproducible commercial pipeline, SQL data model, priority methodology, visual summaries, test suite and consulting memo.
14. **What would you change with more time?** Real authorized aggregate data, multivariate sensitivity on weights, uncertainty intervals and prospectively designed evaluation.
15. **Why a 90-day plan?** It is a manageable illustrative pilot with definition, intervention, monitoring and evaluation stages; actual cadence depends on client context.

## H. Ready-to-say interview answers
### 45-second explanation
“I built a standalone synthetic healthcare commercial strategy case using Python and SQL. I created fictional sales, product, physician-segment and therapy-episode datasets, then calculated revenue, gross profit, margin and aggregate continuity signals. I compared 24 region–product segments using a transparent weighted priority framework and wrote a 90-day validation proposal. I emphasized that this is a simulated decision-support project: the ranking is a shortlist for investigation, not causal proof, clinical advice or a real client result.”

### Why is this relevant to management consulting?
“I started with a business question rather than a visualization. I defined the decision criteria, checked the data grain and unit economics, analyzed different drivers, explicitly documented assumptions and risks, and ended with a recommendation and measurable next steps.”

### If the interviewer challenges the synthetic data
“That's a valid limitation. I chose synthetic data so the project is reproducible and does not reveal personal health information. I am demonstrating the analytical and consulting workflow, not claiming to have discovered actual market or patient outcomes. With authorized real data, I would first verify data governance, medical/compliance requirements, market definitions and causal-study design.”

## I. Your practice exercises
1. Calculate gross margin for revenue INR 50 lakh and COGS INR 32 lakh. Answer: 36%.
2. Calculate contribution after promotion for gross profit INR 18 lakh and promotions INR 4 lakh. Answer: INR 14 lakh.
3. Calculate discontinued share for 72 synthetic discontinued episodes out of 300. Answer: 24%.
4. Write a `GROUP BY region` query for total revenue and gross margin.
5. Write a CTE and `DENSE_RANK` query to find the two highest gross-profit products per region.
6. Explain why a physician table should not be joined to monthly sales on region alone.
7. Change ranking weights to 40/40/10/10, recalculate rankings and explain whether recommendations are stable.
8. Propose a controlled evaluation that avoids claiming that field visits directly cause prescription changes.

## J. How to defend the score when challenged
Run `python -m src.weight_sensitivity`, then inspect `outputs/weight_sensitivity_top5.csv`. The Balanced case is 30/30/20/20. The Financial case is 40/40/10/10. The Investigation case is 20/20/30/30. Compare the top-five segments; if the rankings change materially, explain that the recommended order is sensitive to judgment and that a client workshop is required to calibrate the weights.

## K. SQL JOIN demonstration
Query 6 in `sql/02_analysis_queries.sql` joins sales to the one-row-per-product dimension on `product_id` and groups the result by region and therapy. Because the product dimension has a unique primary key, this many-to-one join does not multiply revenue. Compare this with the unsafe alternative of joining `physicians` to sales on region alone, which would duplicate every region sales record for every physician in that region.
