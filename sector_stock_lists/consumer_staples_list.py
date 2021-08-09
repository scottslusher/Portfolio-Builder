"""Consumer Staples List

This file calculates the top 5 stocks by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_consumer_staples_stocks_by_marketcap(sp500_w_marketcap, consumer_staples, consumer_staples_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    consumer_staples = sp500_w_marketcap.loc["Consumer Staples"]
    consumer_staples_top_5 = consumer_staples.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    consumer_staples_list = consumer_staples_top_5.values.tolist()
    return consumer_staples_list