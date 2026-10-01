-- 1. Regional revenue, gross profit, margins
SELECT region,SUM(revenue_inr) AS revenue_inr,
 SUM(revenue_inr-cogs_inr) AS gross_profit_inr,
 ROUND(1.0*SUM(revenue_inr-cogs_inr)/NULLIF(SUM(revenue_inr),0),4) AS gross_margin
FROM commercial_sales GROUP BY region ORDER BY revenue_inr DESC;

-- 2. Top products by gross profit, with a window rank
WITH product_totals AS (
 SELECT product_id,SUM(revenue_inr) AS revenue_inr,
 SUM(revenue_inr-cogs_inr) AS gross_profit_inr
 FROM commercial_sales GROUP BY product_id
)
SELECT product_id,revenue_inr,gross_profit_inr,
 DENSE_RANK() OVER(ORDER BY gross_profit_inr DESC) AS profit_rank
FROM product_totals ORDER BY profit_rank;

-- 3. Aggregate physician segment whitespace: no real physicians in this dataset
SELECT region,therapy_area,COUNT(*) AS under_engaged_physicians,
 SUM(potential_monthly_rx) AS potential_monthly_rx
FROM physicians WHERE field_visits_last_quarter<3
GROUP BY region,therapy_area ORDER BY potential_monthly_rx DESC;

-- 4. Synthetic day-120 therapy discontinuation rates
SELECT region,product_id,COUNT(*) AS simulated_episodes,
 ROUND(1.0*SUM(CASE WHEN day_120_status='discontinued' THEN 1 ELSE 0 END)/COUNT(*),4) AS discontinuation_rate
FROM synthetic_therapy_episodes GROUP BY region,product_id ORDER BY discontinuation_rate DESC;

-- 5. Region-month sales trend using LAG window function
WITH monthly_sales AS (
 SELECT region,month,SUM(revenue_inr) AS revenue_inr
 FROM commercial_sales GROUP BY region,month
), monthly_changes AS (
 SELECT region,month,revenue_inr,
 LAG(revenue_inr) OVER(PARTITION BY region ORDER BY month) AS prior_month_revenue
 FROM monthly_sales
)
SELECT region,month,revenue_inr,prior_month_revenue,
 ROUND(1.0*(revenue_inr-prior_month_revenue)/NULLIF(prior_month_revenue,0),4) AS month_over_month_change
FROM monthly_changes ORDER BY region,month;

-- 6. JOIN sales to the product dimension: therapy-area commercial economics by region
SELECT s.region,p.therapy_area,SUM(s.revenue_inr) AS revenue_inr,
 SUM(s.revenue_inr-s.cogs_inr) AS gross_profit_inr,
 ROUND(1.0*SUM(s.revenue_inr-s.cogs_inr)/NULLIF(SUM(s.revenue_inr),0),4) AS gross_margin
FROM commercial_sales AS s
JOIN products AS p ON s.product_id=p.product_id
GROUP BY s.region,p.therapy_area
ORDER BY gross_profit_inr DESC;
