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
from sector_stock_lists.industrials_list import top_5_industrial_stocks_by_marketcap

# def sector_return_1_rolling_year ################################################

def sectors(): #CHANGE URL TO PULLING FROM CSV
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_html = pd.read_html(url)
    sp500_html = sp500_html[0]
    sp500_df = pd.DataFrame(sp500_html)
    sp500_all_sectors_df = pd.DataFrame(
        columns=['GICS Sector', 'Symbol'],
        data=sp500_df)
    sectors_1 = sp500_all_sectors_df['GICS Sector'].drop_duplicates().to_list() #POSSIBLE ACTION: dropping the sector that
    sectors_2 = sp500_all_sectors_df['GICS Sector'].drop_duplicates().to_list() # was chosen in the previous function.
    sectors_3 = sp500_all_sectors_df['GICS Sector'].drop_duplicates().to_list() 
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
    print("\n.......................................................................................\n")

    print(".........................pulling data...........please wait..............................\n")

    return np.array([sectors_1, sectors_2, sectors_3])

# def sector_interest_list()

# def initial_investment()



# The following code pulls the list from the csv file and is in every sector list.
#    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
#    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")
# is it worth making a variable?


def data_filter_by_sector():
    # This reads the csv and sets the index to GICS Sector
    sp500_w_marketcap = pd.read_csv(Path("../Resources/stock_industry_marketcap.csv"))
    sp500_w_marketcap = sp500_w_marketcap.set_index("GICS Sector")


def run():
    
    """The main function for running the script"""
    # Get a list of the sector names from the wiki html
    # Be sure to drop duplicate values and capture only unique values.
    # You will use this list of sector names for the user options in the program.

    # STEP 1: Calculate the sectors returns to add to list?
    # STEP 2: Pulling the data and separating out all sp500 sectors
    sectors_1, sectors_2, sectors_3 = sectors()
    
    # STEP 3: runs the sector_interest function
    sector_interest(sectors_1, sectors_2, sectors_3)
    
    # list of stocks as variable to pass to markowitz model

    # value as initial investment





    # STEP ?: LAST STEP
    # Create a variable named running and set it to True
    # running = True
    # # While running is `True` call the `sector_interest` function.
    # while running:
    #     continue_running = sector_interest(sectors_1, sectors_2, sectors_3, url, sp500_html, sp500_df, sp500_all_sectors_df)
    #     if continue_running == 'y':
    #         running = True
    #     else:
    #         running = False

    # return print(type(sectors_1, sectors_2, sectors_3))

# The __main__ loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":
    run()
