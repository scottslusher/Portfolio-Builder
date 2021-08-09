"""Information Technology List

This file calculates the top 5 stocks list by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_information_technology_stocks_by_marketcap(sp500_w_marketcap, information_technology, information_technology_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    information_technology = sp500_w_marketcap.loc["Information Technology"]
    information_technology_top_5 = information_technology.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    information_technology_list = information_technology_top_5.values.tolist()
    return information_technology_list
