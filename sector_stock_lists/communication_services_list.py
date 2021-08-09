"""Communication Services List

This file calculates the top 5 stocks list by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_communicatoin_services_stocks_by_marketcap(sp500_w_marketcap, communication_services, communication_services_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    communication_services = sp500_w_marketcap.loc["Communication Services"]
    communication_services_top_5 = communication_services.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    communication_services_list = communication_services_top_5.values.tolist()
    return communication_services_list