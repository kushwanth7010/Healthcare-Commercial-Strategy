"""Descriptive commercial strategy analysis. Nothing here is clinical advice."""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
OUT=ROOT/"outputs"

def load_data():
    return (pd.read_csv(DATA/"products.csv"),pd.read_csv(DATA/"physicians.csv"),
            pd.read_csv(DATA/"commercial_sales.csv"),pd.read_csv(DATA/"synthetic_therapy_episodes.csv"))


def analyze():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT.mkdir(exist_ok=True)
    product, physician, sale, patient=load_data()
    # Validity assertions before commercial insights.
    assert sale["revenue_inr"].eq(sale["units_sold"]*sale["net_price_inr"]).all()
    assert not sale.duplicated(["month","region","product_id"]).any()
    assert patient["synthetic_episode_id"].is_unique
    merged=sale.merge(product[["product_id","therapy_area"]],on="product_id",validate="many_to_one")
    merged["gross_profit_inr"]=merged["revenue_inr"]-merged["cogs_inr"]
    merged["contribution_inr"]=merged["gross_profit_inr"]-merged["promotion_spend_inr"]
    merged.to_csv(OUT/"sales_enriched.csv",index=False)
    by_region=merged.groupby("region",as_index=False)[["revenue_inr","gross_profit_inr","contribution_inr","promotion_spend_inr","units_sold","sales_calls","prescriptions"]].sum()
    by_region["gross_margin"]=by_region["gross_profit_inr"]/by_region["revenue_inr"]
    by_region["revenue_per_call_inr"]=by_region["revenue_inr"]/by_region["sales_calls"]
    by_region.to_csv(OUT/"regional_performance.csv",index=False)
    group_cols=["region","product_id","therapy_area"]
    segment=merged.groupby(group_cols,as_index=False).agg(revenue_inr=("revenue_inr","sum"),
        gross_profit_inr=("gross_profit_inr","sum"),contribution_inr=("contribution_inr","sum"),
        promotion_spend_inr=("promotion_spend_inr","sum"),units_sold=("units_sold","sum"),
        sales_calls=("sales_calls","sum"),prescriptions=("prescriptions","sum"))
    segment["gross_margin"]=segment["gross_profit_inr"]/segment["revenue_inr"]
    segment["revenue_per_call_inr"]=segment["revenue_inr"]/segment["sales_calls"]
    physician["under_engaged"]=physician["field_visits_last_quarter"]<3
    whitespace=(physician[physician["under_engaged"]]
       .groupby(["region","therapy_area"],as_index=False)["potential_monthly_rx"].sum()
       .rename(columns={"potential_monthly_rx":"under_engaged_potential_monthly_rx"}))
    segment=segment.merge(whitespace,on=["region","therapy_area"],how="left",validate="many_to_one")
    segment["under_engaged_potential_monthly_rx"]=segment["under_engaged_potential_monthly_rx"].fillna(0)
    patient["discontinued"]=patient["day_120_status"].eq("discontinued")
    continuity=(patient.groupby(["region","product_id"],as_index=False)
       .agg(synthetic_episode_count=("synthetic_episode_id","count"),discontinuation_rate=("discontinued","mean")))
    segment=segment.merge(continuity,on=["region","product_id"],how="left",validate="one_to_one")
    assert not segment.isna().any().any(), "Synthetic coverage must include all 24 segments"
    # Simple percentile ranking of opportunity proxies. Weights are illustrative management assumptions.
    weights={"revenue_inr":.30,"gross_margin":.30,
             "under_engaged_potential_monthly_rx":.20,"discontinuation_rate":.20}
    for field in weights:
        segment[field+"_percentile"]=segment[field].rank(pct=True,method="average")
    segment["priority_score_100"]=sum(segment[name+"_percentile"]*weight*100 for name,weight in weights.items())
    segment["priority_rank"]=segment["priority_score_100"].rank(method="first",ascending=False).astype(int)
    segment=segment.sort_values("priority_rank").reset_index(drop=True)
    segment.to_csv(OUT/"segment_prioritization.csv",index=False)
    totals={"revenue_inr":int(merged["revenue_inr"].sum()),"gross_profit_inr":int(merged["gross_profit_inr"].sum()),
            "gross_margin":merged["gross_profit_inr"].sum()/merged["revenue_inr"].sum(),
            "contribution_after_promotion_inr":int(merged["contribution_inr"].sum()),
            "sales_calls":int(merged["sales_calls"].sum()),"prescriptions":int(merged["prescriptions"].sum()),
            "synthetic_episode_count":len(patient),"discontinuation_rate":float(patient["discontinued"].mean())}
    pd.DataFrame([totals]).to_csv(OUT/"executive_kpis.csv",index=False)
    plt.figure(figsize=(8,4.5))
    plt.bar(by_region["region"],by_region["revenue_inr"]/10_000_000)
    plt.ylabel("Synthetic revenue (INR crore)")
    plt.title("Regional commercial scale")
    plt.tight_layout()
    plt.savefig(OUT/"regional_revenue.png",dpi=170)
    plt.close()
    top=segment.head(8)
    plt.figure(figsize=(9,4.8))
    plt.barh((top["region"]+" | "+top["product_id"])[::-1],top["priority_score_100"][::-1])
    plt.xlabel("Illustrative priority score (0–100)")
    plt.title("Commercial opportunity prioritization")
    plt.tight_layout()
    plt.savefig(OUT/"priority_segments.png",dpi=170)
    plt.close()
    first=segment.head(3)
    memo=["# Executive strategy brief | Synthetic healthcare commercial portfolio","",
          "**Question:** Where could a commercial team investigate resource reallocation across regions/products while considering profit, channel whitespace and therapy-continuation signals?","",
          "**Scope:** Educational simulation. All physicians, product labels, transactions and therapy episodes are synthetic. No clinical decisions or individual patient targeting are supported.","",
          "## Portfolio snapshot",
          f"- Revenue: INR {totals['revenue_inr']/10_000_000:,.2f} crore",
          f"- Gross profit: INR {totals['gross_profit_inr']/10_000_000:,.2f} crore",
          f"- Gross margin: {totals['gross_margin']:.1%}",
          f"- Gross profit after promotion spend: INR {totals['contribution_after_promotion_inr']/10_000_000:,.2f} crore (not a full operating-profit measure)",
          f"- Synthetic therapy episodes: {totals['synthetic_episode_count']:,}; simulated day-120 discontinuation: {totals['discontinuation_rate']:.1%}","",
          "## Highest model-ranked region–product segments (exploratory)","",
          "| Segment | Revenue (INR crore) | Gross margin | Simulated discontinuation | Score |",
          "|---|---:|---:|---:|---:|"]
    for _,row in first.iterrows():
        memo.append(f"| {row['region']} / {row['product_id']} | {row['revenue_inr']/10_000_000:.2f} | {row['gross_margin']:.1%} | {row['discontinuation_rate']:.1%} | {row['priority_score_100']:.1f} |")
    memo += ["","## Proposed 90-day validation pilot",
             "1. **Days 1–15:** Review definitions, validate assumptions with finance/commercial/medical/compliance teams and establish comparable region/product baselines.",
             "2. **Days 16–45:** Test commercial resource scheduling for high-potential, low-engagement *physician segments*, subject to ethical promotion and local policy.",
             "3. **Days 46–70:** Review clinician-approved, non-personalized patient support communications where permitted; do not infer therapy effectiveness from commercial data.",
             "4. **Days 71–90:** Compare pre-defined revenue, gross margin, sales-call efficiency and aggregate continuity KPIs against a suitable comparison group before scaling.","",
             "## Limits and risks",
             "- Priority scores are weighted decision aids, not validated causal or clinical outcomes.",
             "- Revenue is a proxy for current commercial scale, not a defensible market-size estimate.",
             "- Under-engaged physician potential is synthetic and does not imply prescriptions can be won by adding visits.",
             "- Higher discontinuation here flags a topic for clinical investigation, not evidence that a product or clinician performed poorly.",
             "- The patient-episode and sales datasets are independently simulated, not reconciled longitudinal real-world evidence."]
    (OUT/"executive_strategy_brief.md").write_text("\n".join(memo)+"\n",encoding="utf-8")
    print("EXECUTIVE_KPIS",totals)
    print("TOP_SEGMENTS\n",segment[["region","product_id","priority_score_100"]].head(5).to_string(index=False))
    return segment,totals

if __name__ == "__main__": analyze()
