"""Check whether the segment shortlist is stable across illustrative weights."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS={
    "Balanced":{"revenue_inr":.30,"gross_margin":.30,"under_engaged_potential_monthly_rx":.20,"discontinuation_rate":.20},
    "Financial emphasis":{"revenue_inr":.40,"gross_margin":.40,"under_engaged_potential_monthly_rx":.10,"discontinuation_rate":.10},
    "Investigation emphasis":{"revenue_inr":.20,"gross_margin":.20,"under_engaged_potential_monthly_rx":.30,"discontinuation_rate":.30},
}

def compare():
    data=pd.read_csv(ROOT/"outputs"/"segment_prioritization.csv")
    rows=[]
    for name,weight in WEIGHTS.items():
        if abs(sum(weight.values())-1)>1e-8:
            raise ValueError("Weights must total 100%")
        data["case_score"]=100*sum(data[k+"_percentile"]*v for k,v in weight.items())
        for i,row in data.sort_values("case_score",ascending=False).head(5).reset_index(drop=True).iterrows():
            rows.append({"weight_case":name,"rank":i+1,"region":row["region"],
                         "product_id":row["product_id"],"score":row["case_score"]})
    result=pd.DataFrame(rows)
    result.to_csv(ROOT/"outputs"/"weight_sensitivity_top5.csv",index=False)
    print(result.to_string(index=False))
    return result

if __name__=="__main__":compare()
