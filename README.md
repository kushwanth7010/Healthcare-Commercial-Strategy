# Healthcare Commercial Strategy & Market Prioritization

**Synthetic consulting portfolio case · Python · SQL/SQLite · Excel · KPI analysis · business recommendations**

This is an independent **synthetic-data case study**. No real patients, physician identities, protected health information, client assignments or actual clinical conclusions are involved.

## Business question
How can a hypothetical healthcare commercial team investigate which regions and products merit further investment, given competing revenue, profit, physician-engagement and patient-continuity considerations?

## Project workflow
1. Generate synthetic commercial sales, physicians, product and therapy-episode data.
2. Validate and join the datasets, evaluate revenue, gross profit, margin, contribution and physician-engagement proxies.
3. Create a SQLite database and run analyst-friendly SQL queries.
4. Summarize 24 region–product segments in a transparent weighted strategy scorecard.
5. Test how changing the decision weights changes the shortlist; translate results into a controlled 90-day pilot proposal.
6. Document privacy, medical, causal-inference and strategy limitations.

## Run
```bash
python -m pip install -r requirements.txt
python -m src.generate_data
python -m src.analyze
python -m src.build_sqlite
python -m src.run_sql_queries
python -m src.weight_sensitivity
python -m unittest discover -s tests -v
```

Inputs are **fully synthetic**. Weighted prioritization is a decision aid, not clinical advice or an automatic direction to target patients. Review the project documentation and notebooks/outputs before using any results in a resume or interview.

**Portfolio purpose:** demonstrate consulting problem definition, quantitative business analysis, prioritization, transparent assumptions, SQL and implementable recommendations.
