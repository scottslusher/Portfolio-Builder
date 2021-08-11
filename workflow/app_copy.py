# A Database CLI Application

# Import modules
import pandas as pd
import sqlalchemy as sql
import os
import questionary
import yfinance as yf
from pathlib import Path
import csv
import fire
import requests
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import datetime as dt
from datetime import date
# from MCForecastTools import MCSimulation

# importing sector lists of stocks from 'sector_stock_lists' folder
# from sector_stock_lists.industrials_list import top_5_industrial_stocks_by_marketcap

# def sector_return_1_rolling_year ################################################

def stock_generator(sectors):
    database_connection_string = 'sqlite:///stock_industry_top5.db'
    engine = sql.create_engine(database_connection_string, echo=True)
    # stocks_df = pd.read_csv(Path('resources/stock_industry_marketcap.csv')).sort_values("Market_Cap", ascending=False)
    # stocks_df.to_sql('stocks_by_marketcap', engine, index=False, if_exists='replace')
    sql_stock_df = pd.read_sql_table('stock_by_marketcap', con=engine)
    # stocks = []

    sectors = sql_stock_df['Symbol']

    for x in sectors:
        top_5_stocks = f"""
        SELECT Symbol
        FROM stocks_by_marketcap
        WHERE 'GICS Sector' = '{x}'
        ORDER BY Market_Cap DESC
        LIMIT 5
        """
        results = engine.execute(top_5_stocks)
        stocks.append(list(results))

    return stocks

def clean_stock_list(stocks):
    clean_stocks = []
    for ch in ['(',',)']:
        if ch in stocks:
            stocks = stocks.replace(ch,'')
            clean_stocks.append(stocks)
    return clean_stocks



def sectors(): 
    csvpath = Path("./resources/stock_industry_marketcap.csv")
    sp500_csv = pd.read_csv(csvpath)
    sector = "GICS Sector"
    sp500_sectors = sp500_csv[sector].drop_duplicates().to_list()
    sectors_1 = sp500_sectors #POSSIBLE ACTION: dropping the sector that
    sectors_2 = sp500_sectors
    sectors_3 = sp500_sectors 
    return sectors_1, sectors_2, sectors_3

# Create a function called `sector_interest` that will be the application report.
# This function will be called from the __main__ loop.
def sector_interest(sectors_1, sectors_2, sectors_3):

    # Print welcome message and short description of what the program will output.
    print("\n................**Welcome to the Sector Portfolio Builder!**................................\n")
    print("Based on the three sectors you choose, the program will calculate the optimal portoflio\n")
    print("of stocks within the three sectors including weights of each. After optimal portfolio is\n")
    print("calculated, data points for rolling 1-year, 3-year, 5-year and 10-year returns as well\n")
    print("as expected returns, volatility and sharpe ratio's.")

    print("\n.......................................................................................\n")
    # Using questionary, select 1st sector
    sectors_1 = questionary.select("What is the 1st sector your interested in?", choices=sectors_1).ask()
    sectors_2 = questionary.select("What is the 2nd sector your interested in?", choices=sectors_2).ask()
    sectors_3 = questionary.select("What is the 3rd sector your interested in?", choices=sectors_3).ask()
    
    print("The following stocks are the top 5 stocks by marketcap in each sector")
    sectors_selected = np.array([sectors_1, sectors_2, sectors_3])
    return sectors_selected

def investment_question():
    investment = questionary.text("How much money would you like to invest?").ask()
    print("\n.......................................................................................\n")

    print(".........................pulling data...........please wait..............................\n")
    return int(investment)

