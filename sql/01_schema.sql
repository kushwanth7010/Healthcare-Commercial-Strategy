-- SQLite schema for synthetic commercial healthcare case, no personal information.
CREATE TABLE IF NOT EXISTS products (
 product_id TEXT PRIMARY KEY, therapy_area TEXT NOT NULL,
 list_price_inr INTEGER NOT NULL,unit_cogs_inr INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS physicians (
 physician_id TEXT PRIMARY KEY, region TEXT NOT NULL,
 therapy_area TEXT NOT NULL, potential_monthly_rx INTEGER NOT NULL,
 field_visits_last_quarter INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS commercial_sales (
 month TEXT NOT NULL, region TEXT NOT NULL, product_id TEXT NOT NULL,
 units_sold INTEGER NOT NULL,net_price_inr INTEGER NOT NULL,
 revenue_inr INTEGER NOT NULL,cogs_inr INTEGER NOT NULL,
 promotion_spend_inr INTEGER NOT NULL,sales_calls INTEGER NOT NULL,
 prescriptions INTEGER NOT NULL,
 PRIMARY KEY(month,region,product_id),FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE TABLE IF NOT EXISTS synthetic_therapy_episodes (
 synthetic_episode_id TEXT PRIMARY KEY,region TEXT NOT NULL,
 product_id TEXT NOT NULL,cohort_start_month TEXT NOT NULL,
 day_120_status TEXT NOT NULL, observed_days INTEGER NOT NULL,
 FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE INDEX IF NOT EXISTS idx_sales_region_product ON commercial_sales(region, product_id);
CREATE INDEX IF NOT EXISTS idx_physician_region_therapy ON physicians(region, therapy_area);
CREATE INDEX IF NOT EXISTS idx_episode_region_product ON synthetic_therapy_episodes(region, product_id);
