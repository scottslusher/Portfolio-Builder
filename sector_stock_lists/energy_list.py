"""Energy List

This file calculates the top 5 stocks by marketcap

"""
# Import modules
import csv
from pathlib import Path
import pandas as pd

def top_5_energy_stocks_by_marketcap(sp500_w_marketcap, energy, energy_top_5):
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
    energy = sp500_w_marketcap.loc["Energy"]
    energy_top_5 = energy.set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    energy_list = energy_top_5.values.tolist()
    return energy_list