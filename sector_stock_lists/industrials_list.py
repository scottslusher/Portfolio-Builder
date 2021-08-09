"""Industrials List

This file calculates the top 5 stocks by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_industrial_stocks_by_marketcap(sp500_w_marketcap, industrials, industrials_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    industrials = sp500_w_marketcap.loc["Industrials"]
    industrials_top_5 = industrials.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    industrials_list = industrials_top_5.values.tolist()
    return industrials_list


