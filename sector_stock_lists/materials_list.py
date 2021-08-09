"""Materials List

This file calculates the top 5 stocks by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_materials_stocks_by_marketcap(sp500_w_marketcap, materials, materials_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    materials = sp500_w_marketcap.loc["Materials"]
    materials_top_5 = materials.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    materials_list = materials_top_5.values.tolist()
    return materials_list