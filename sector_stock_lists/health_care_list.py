"""Health Care List

This file calculates the top 5 stocks list by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_health_care_stocks_by_marketcap(sp500_w_marketcap, health_care, health_care_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    health_care = sp500_w_marketcap.loc["Health Care"]
    health_care_top_5 = health_care.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    health_care_list = health_care_top_5.values.tolist()
    return health_care_list