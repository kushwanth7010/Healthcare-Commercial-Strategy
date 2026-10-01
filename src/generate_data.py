"""Create deterministic, wholly synthetic commercial and patient-episode datasets."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RNG_SEED = 20261001
REGIONS = ["North", "South", "East", "West"]
PRODUCTS = [
    ("CARD-A", "Cardiology", 950, 410),
    ("CARD-B", "Cardiology", 1240, 510),
    ("META-A", "Metabolic", 730, 310),
    ("META-B", "Metabolic", 1100, 450),
    ("RESP-A", "Respiratory", 850, 390),
    ("RESP-B", "Respiratory", 1050, 450),
]


def generate_all(seed=RNG_SEED):
    rng=np.random.default_rng(seed)
    DATA.mkdir(exist_ok=True)
    product_df=pd.DataFrame(PRODUCTS,columns=["product_id","therapy_area","list_price_inr","unit_cogs_inr"])
    product_df.to_csv(DATA/"products.csv",index=False)
    doctors=[]
    specialties=["Cardiology", "Metabolic", "Respiratory"]
    for region in REGIONS:
        for speciality in specialties:
            for _ in range(20):
                doc_id=f"DR{len(doctors)+1:04d}"
                potential=int(rng.integers(45,190))
                calls=int(rng.integers(0,13))
                doctors.append({"physician_id":doc_id,"region":region,"therapy_area":speciality,
                    "potential_monthly_rx":potential,"field_visits_last_quarter":calls})
    doctor_df=pd.DataFrame(doctors)
    doctor_df.to_csv(DATA/"physicians.csv",index=False)
    region_factors={"North":1.16,"South":1.08,"East":.89,"West":1.03}
    product_factors={"CARD-A":1.05,"CARD-B":.81,"META-A":1.23,"META-B":.96,"RESP-A":1.14,"RESP-B":.87}
    sales=[]
    for month in range(1,13):
        for region in REGIONS:
            for product,therapy,price,cogs in PRODUCTS:
                seasonality=1+.06*np.sin(2*np.pi*(month-1)/12)
                units=int(max(100,round(740*region_factors[region]*product_factors[product]*seasonality*rng.uniform(.81,1.19))))
                net_price=int(round(price*rng.uniform(.93,1.02)))
                revenue=units*net_price
                cogs_total=units*cogs
                promo_spend=int(round(revenue*rng.uniform(.055,.115)))
                calls=int(rng.integers(45,145))
                prescriptions=int(max(0,round(units*rng.uniform(.74,.94))))
                sales.append({"month":f"2025-{month:02d}","region":region,"product_id":product,
                              "units_sold":units,"net_price_inr":net_price,"revenue_inr":revenue,
                              "cogs_inr":cogs_total,"promotion_spend_inr":promo_spend,
                              "sales_calls":calls,"prescriptions":prescriptions})
    sales_df=pd.DataFrame(sales)
    sales_df.to_csv(DATA/"commercial_sales.csv",index=False)
    patient=[]
    for index in range(1,8001):
        product, therapy, price, cogs=PRODUCTS[int(rng.integers(0,len(PRODUCTS)))]
        region=REGIONS[int(rng.integers(0,4))]
        baseline={"Cardiology":.20,"Metabolic":.26,"Respiratory":.23}[therapy]
        mod={"North":.015,"South":-.02,"East":.045,"West":0}[region]
        discontinuation=bool(rng.random()<(baseline+mod))
        days=int(rng.integers(18,120)) if discontinuation else 120
        patient.append({"synthetic_episode_id":f"EP{index:05d}","region":region,"product_id":product,
                        "cohort_start_month":f"2025-{int(rng.integers(1,10)):02d}",
                        "day_120_status":"discontinued" if discontinuation else "continuing",
                        "observed_days":days})
    patient_df=pd.DataFrame(patient)
    patient_df.to_csv(DATA/"synthetic_therapy_episodes.csv",index=False)
    print(f"GENERATED {len(sales_df)} sales rows, {len(doctor_df)} synthetic physicians, {len(patient_df)} synthetic episodes")
    return product_df, doctor_df, sales_df, patient_df

if __name__=="__main__": generate_all()
