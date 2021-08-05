# A Database CLI Application

# Import modules
import pandas as pd
import sqlalchemy as sql
import os
import questionary
import yfinance as yf
from pathlib import Path
import csv
import requests
import numpy as np

# Create a function called `sector_interest` that will be the application report.
# This function will be called from the __main__ loop.
def sector_interest(sectors, url, sp500_html, sp500_df, sp500_all_sectors_df):

    # Print welcome message and short description of what the program will output.
    print("\n................Welcome to the sector portfolio builder................................\n")
    print("Based on the three sectors you choose, the program will calculate the optimal portoflio\n")
    print("of stocks within the three sectors including weights of each. After optimal portfolio is\n")
    print("calculated, data points for rolling 1-year, 3-year, 5-year and 10-year returns as well\n")
    print("as expected returns, volatility and sharpe ratio's.")

    print("\n.......................................................................................\n")
    # Using questionary, select 3 sectors
    sectors = questionary.select("Which 3 sectors are you interested in?", choices=sectors).ask()
    print("\n.......................................................................................\n")

    print(".........................pulling data...........please wait..............................\n")

    # Pulling S&P Data from wiki and outputing html
    # Sepecify URL, read html from wiki website
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_html = pd.read_html(url)
    # Obtain first table
    sp500_html = sp500_html[0]
    # Create dataframe
    sp500_df = pd.DataFrame(sp500_html)
    # Save file to CSV
    sp500_df.to_csv("sp500_wiki_table.csv")
    # Separate out table to GISC Sector and Symbol
    sp500_all_sectors_df = pd.DataFrame(
        columns=['GICS Sector', 'Symbol'],
        data=sp500_df)
    # Create list of sectors in the S&P 500
    sectors = sp500_all_sectors_df['GICS Sector'].drop_duplicates().to_list()


# The __main__ loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":


    # Get a list of the sector names from the `nyse_df` DataFrame
    # Be sure to drop n/a values and capture only unique values.
    # You will use this list of sector names for the user options in the report.
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_html = pd.read_html(url)
    sp500_html = sp500_html[0]
    sp500_df = pd.DataFrame(sp500_html)
    sp500_all_sectors_df = pd.DataFrame(
        columns=['GICS Sector', 'Symbol'],
        data=sp500_df)
    sectors = sp500_all_sectors_df['GICS Sector'].drop_duplicates().to_list()
    sectors = sectors

    # Create a variable named running and set it to True
    running = True

    # While running is `True` call the `sector_interest` function.
    # Pass the `nyse_df` DataFrame `sectors` and the database `engine` as parameters.
    while running:
        continue_running = sector_interest(sectors, url, sp500_html, sp500_df, sp500_all_sectors_df)
        if continue_running == 'y':
            running = True
        else:
            running = False
