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

def stock_generator(sectors):
    database_connection_string = 'sqlite:///stock_industry_top5.db'
    engine = sql.create_engine(database_connection_string, echo=True)
    stocks_df = pd.read_csv(Path('stock_industry_marketcap.csv'))
    stocks_df.to_sql('stock_industry_marketcap', engine, index=False, if_exists='replace')
    sql_stock_df = pd.read_sql_table('stock_industry_marketcap', con=engine)
    stocks = []
    for x in sectors:
        top_5_stocks = f"""
        SELECT Symbol
        FROM stocks_by_marketcap
        WHERE 'GICS Sector' = '{x}'
        ORDER BY Market_Cap DESC
        LIMIT 5
        """
        results = engine.execute(top_5_stocks)
        data = pd.DataFrame(data=results)
        stocks.append(data)
    return stocks





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
def sector_interest(sectors):

    # # Print welcome message and short description of what the program will output.
    # print("\n................**Welcome to the Sector Portfolio Builder!**................................\n")
    # print("Based on the three sectors you choose, the program will calculate the optimal portoflio\n")
    # print("of stocks within the three sectors including weights of each. After optimal portfolio is\n")
    # print("calculated, data points for rolling 1-year, 3-year, 5-year and 10-year returns as well\n")
    # print("              as expected returns, volatility and sharpe ratio's.")

    # print("\n.......................................................................................\n")
    # Using questionary, select 1st sector
    sectors_1 = questionary.select("What is the 1st sector your interested in?", choices=sectors).ask()
    sectors_2 = questionary.select("What is the 2nd sector your interested in?", choices=sectors).ask()
    sectors_3 = questionary.select("What is the 3rd sector your interested in?", choices=sectors).ask()
    sectors_selected = np.array([sectors_1, sectors_2, sectors_3])
    return sectors_selected

def investment_question():
    investment = questionary.text("How much money would you like to invest?").ask()
    #print("\n.......................................................................................\n")

    #print(".........................pulling data...........please wait..............................\n")
    return int(investment)

def generate_tickers(sectors):
    # Create a database connection string that links an in-memory database
    database_connection_string = 'sqlite:///stock_industry_top5.db'

    # Database connection object
    engine = sql.create_engine(database_connection_string)

    # Confirm the engine was created
    engine
    
    stocks_df = pd.read_csv(
    Path('resources/stock_industry_marketcap.csv')
    )

    stocks_df.to_sql('stock_industry_marketcap', engine, index=False, if_exists='replace')

    sql_stock_df = pd.read_sql_table('stock_industry_marketcap', con=engine)
   
    l1 = sectors[0]
    top5_1 = f"""
    SELECT Symbol
    FROM stock_industry_marketcap
    WHERE `GICS Sector` = '{l1}'
    ORDER BY Market_Cap DESC
    LIMIT 5
    """
    results_1 = engine.execute(top5_1)
    data_1 = pd.DataFrame(results_1)

    l2 = sectors[1]
    top5_2 = f"""
    SELECT Symbol
    FROM stock_industry_marketcap
    WHERE `GICS Sector` = '{l2}'
    ORDER BY Market_Cap DESC
    LIMIT 5
    """
    results_2 = engine.execute(top5_2)
    data_2 = pd.DataFrame(results_2)

    l3 = sectors[2]
    top5_3 = f"""
    SELECT Symbol
    FROM stock_industry_marketcap
    WHERE `GICS Sector` = '{l3}'
    ORDER BY Market_Cap DESC
    LIMIT 5
    """
    results_3 = engine.execute(top5_3)
    data_3 = pd.DataFrame(results_3)

    clean_symbols = pd.concat([data_1, data_2, data_3], axis="rows", join="inner")
    symbols = clean_symbols[0].tolist()
    return symbols
