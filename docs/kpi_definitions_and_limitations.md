# KPI dictionary and data integrity

| KPI | Definition | Caution |
|---|---|---|
| Revenue | SUM(units_sold × net_price_inr) | Synthetic booked sales only |
| COGS | SUM(cogs_inr) | Simulated cost of sold units |
| Gross profit | Revenue − COGS | Excludes promotion and corporate expenses |
| Gross margin | Gross profit / Revenue | Descriptive, not a future margin guarantee |
| Contribution after promotion | Gross profit − promotion_spend_inr | Not full operating profit; excludes overhead, sales salaries etc. |
| Revenue per sales call | Revenue / sales_calls | Observational ratio; **not** marginal return caused by calls |
| Physician whitespace | SUM(potential_monthly_rx) for synthetic physicians with fewer than 3 visits last quarter, grouped by region and therapy | Synthetic potential estimate, not a claim that more visits cause prescriptions |
| Day-120 discontinuation | Synthetic episode rows labeled `discontinued` / all episodes in the group | Simulated status; **not** a measured clinical adherence or effectiveness outcome |
| Priority score | Weighted sum of percentile ranks of four defined business/opportunity proxies | Subjective weights; percentile comparison across 24 simulated region–product groups |

## Why this dataset is explicitly synthetic
The generator uses a fixed random seed and **fictional labels**. There are no real doctor names, patient names, emails, record IDs, diagnosis details or personally identifying fields. All episode IDs and doctor IDs are generated from counters.

## What the dataset cannot establish
- No medical efficacy, safety, diagnosis, prescribing recommendation, individual patient care or causal effect.
- No actual healthcare-provider performance or territory performance.
- No defensible total-addressable-market (TAM) value or competitive market share.
- No ROI from promotional spending: promotional cost and revenue may be correlated but causality is not identified.
- No reconciliation between aggregate commercial sales and independent synthetic episode data.

## Real-world requirements for a valid client study
Proper rights to data, privacy/security review, legal/compliance review, anonymization, validated cohort definitions, clinical governance, data provenance, consistent time windows, payer/reimbursement context, external market data, and an explicitly designed experimental or quasi-experimental evaluation.
