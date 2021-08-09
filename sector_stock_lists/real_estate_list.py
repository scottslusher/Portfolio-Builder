"""rReal Estate List

This file calculates the top 5 stocks by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_real_estate_stocks_by_marketcap(sp500_w_marketcap, real_estate, real_estate_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    real_estate = sp500_w_marketcap.loc["Real Estate"]
    real_estate_top_5 = real_estate.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    real_estate_list = real_estate_top_5.values.tolist()
    return real_estate_list