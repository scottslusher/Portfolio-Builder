"""Consumer Discretionary List

This file calculates the top 5 stocks list by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def consumer_discretionary_top_5_stocks_by_marketcap(sp500_w_marketcap, consumer_discretionary, consumer_discretionary_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    consumer_discretionary = sp500_w_marketcap.loc["Consumer Discretionary"]
    consumer_discretionary_top_5 = consumer_discretionary.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    consumer_discretionary_list = consumer_discretionary_top_5.values.tolist()
    return consumer_discretionary_list