import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.generate_data import generate_all
from src.analyze import analyze,load_data

class HealthcareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate_all()
        cls.segment,cls.total=analyze()
    def test_unique_complete_panel(self):
        _,_,sales,episodes=load_data()
        self.assertEqual(len(sales),288)
        self.assertEqual(len(episodes),8000)
        self.assertFalse(sales.duplicated(["month","region","product_id"]).any())
    def test_revenue_reconciles(self):
        _,_,sale,_=load_data()
        self.assertEqual(sale["revenue_inr"].sum(),self.total["revenue_inr"])
        self.assertTrue((sale["revenue_inr"]==sale["units_sold"]*sale["net_price_inr"]).all())
    def test_profit_and_scores(self):
        self.assertEqual(len(self.segment),24)
        self.assertTrue(self.segment["priority_score_100"].between(0,100).all())
        self.assertEqual(self.segment["priority_rank"].iloc[0],1)
        self.assertTrue(self.segment["gross_margin"].between(0,1).all())
    def test_synthetic_episode_status(self):
        _,_,_,episodes=load_data()
        self.assertTrue(episodes["day_120_status"].isin(["continuing","discontinued"]).all())
        self.assertTrue(episodes["synthetic_episode_id"].is_unique)
    def test_reproducibility(self):
        before=self.total["revenue_inr"]
        generate_all()
        _,_,sale,_=load_data()
        self.assertEqual(before,sale["revenue_inr"].sum())

if __name__=="__main__":unittest.main()
