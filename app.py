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
    print("\n.......................................................................................\n")

    print(".........................pulling data...........please wait..............................\n")

    return np.array([sectors_1, sectors_2, sectors_3])

# This function sorts the stocks in the sp500 by marketcap in descending order with sector as index
def stocks(sp500_csv):
    sp500_stocks_sorted = sp500_csv.set_index("GICS Sector").sort_values("Market_Cap", ascending=False)
    return sp500_stocks_sorted

#### TESTING ######
def chosen_sectors(sp500_stocks_sorted, sectors_1, sectors_2, sectors_3):
    # Slices the lists into sector variables containing the top 5 stocks by marketcap

    industrials = sp500_stocks_sorted.loc["Industrials"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    health_care = sp500_stocks_sorted.loc["Health Care"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    information_technology = sp500_stocks_sorted.loc["Information Technology"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    communication_services = sp500_stocks_sorted.loc["Communication Services"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    consumer_discretionary = sp500_stocks_sorted.loc["Consumer Discretionary"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    utilities = sp500_stocks_sorted.loc["Utilities"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    financials = sp500_stocks_sorted.loc["Financials"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    materials = sp500_stocks_sorted.loc["Materials"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    real_estate = sp500_stocks_sorted.loc["Real Estate"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    consumer_staples = sp500_stocks_sorted.loc["Consumer Staples"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    energy = sp500_stocks_sorted.loc["Energy"].sort_values(by="Market_Cap", ascending=False).iloc[0:5]
    
    rows = csv.reader(sp500_stocks_sorted)
    header = next(rows)
    sector = sectors_1, sectors_2, sectors_3
    for sector in sector_interest:
        if sector == industrials:
            return list(industrials["Symbol"])
        elif sector == health_care:
            return list(health_care["Symbol"])
        elif sector == information_technology:
            return list(information_technology["Symbol"])
        elif sector == communication_services:
            return list(communication_services["Symbol"])
        elif sector == consumer_discretionary:
            return list(consumer_discretionary["Symbol"])
        elif sector == utilities:
            return list(utilities["Symbol"])
        elif sector == financials:
            return list(financials["Symbol"])
        elif sector == materials:
            return list(materials["Symbol"])
        elif sector == real_estate:
            return list(real_estate["Symbol"])
        elif sector == consumer_staples:
            return list(consumer_staples["Symbol"])
        elif sector == energy:
            return list(energy["Symbol"])
        else:
            return print("Unable to pick stocks.")





################################################################################################################
# MARKOWITZ MODEL:

# we want the user to focus on the assets they are wanting to analyze and not the amount of data the program is analyzing
# so in order to get the most relevant information we create a dynamic date range with a rolling 10 year window
# first we create a variable today and set it equal to the datetime libraries date.today() 
today = date.today()

# once we have todays date we can run a formula to replace the year output from the date.today() with whatever timeframe we enter
# in our program we will set this input at 10 years
def sub_years(today_date, years):
    try:
        return today_date.replace(year = today_date.year - years)
    except ValueError:
        return today_date + (date(today_date.year + years, 1, 1) - date(today_date.year, 1, 1))

# historical data - define START and END dates
# to calculate the start_date we must use the sub_years function defined above to get today's date and subtract 10 years
# then using the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance
start_date = sub_years(today, 10).strftime('%Y-%m-%d')
# for the end_date we just have to reformat the today variable with the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance 
end_date = today.strftime('%Y-%m-%d')

### IF WE ARE GOING TO ALLOW CRYPTO THEN WE NEED TO UPDATE THE TRADING DAYS TO 365 AND RERUN THE CALCS

# number of trading days in a year (stocks only)
num_tradings_days_stocks = 252
num_tradings_days_crypto = 365

# set variable of amount of random w (different portfolios) we want to create
num_portfolios = 20000

# define a function download_data()
def download_data(stocks):
    stock_data = yf.download(
        #tickers list or string as well
        tickers = stocks,

        # use "period" instead of start/end
        # valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        # (optional, default is "1mo")
        period = "10y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = '1d',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integre)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )['Close']

    return pd.DataFrame(stock_data)

# define a function show_data()
def show_data(data):
    data.plot(figsize=(20,10), grid=True, xlabel='Date', ylabel="Stock Price", title=f"Historical Price from {start_date} through {end_date}")
    plt.show()

# define return
def calculate_log_return(data):
    # NORMALIZATION - to measure all variables in comparable metric
    log_return = np.log(data/data.shift(1))
    # return [1:] takes out the null values from the first data point
    return log_return[1:]

def calculate_return(data):
    daily_returns = data.pct_change()
    return daily_returns[1:]

# define annual metrics
def show_statistics(returns):
    print(returns.mean() * num_tradings_days)
    print(returns.cov() * num_tradings_days)

#
def show_mean_variance(returns, weights):
    portfolio_return = np.sum(returns.mean()*weights) * num_tradings_days_stocks
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*num_tradings_days_stocks, weights)))
    print(f"Expected portfolio mean (return): {portfolio_return}")
    print(f"Expected portfolio volatilit (standard deviation): {portfolio_volatility}")


def generate_portfolios(returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(num_portfolios):
        # w = np.random.random(len(stocks))
        w = sp500_stock
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * num_tradings_days_stocks)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * num_tradings_days_stocks, w))))
    
    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(20,10))
    plt.scatter(volatilities, returns, c=returns/volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Returns')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * num_tradings_days_stocks
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * num_tradings_days_stocks, weights)))

    return np.array([portfolio_return, portfolio_volatility, portfolio_return/portfolio_volatility])

# scipy optimize module can find the minimum of a given function
# the maximum of a f(x) is the minimum of -f(x)
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# what are the constraints? the sum of weights = 1
# f(x)=0 this is the function to minimize
def optimize_portfolio(weights, returns):
    # the sum of weights is 1
    cons = {'type': 'eq', 'fun': lambda x: np.sum(x) -1}
    # the weights can be 1 at most: 1 when 100% of money is invested inot a single stock
    bnds = tuple((0,1) for _ in range(len(stocks)))
    
    return optimization.minimize(
                fun=min_function_sharpe,
                x0=weights[0],
                args=returns,
                method='SLSQP',
                bounds=bnds,
                constraints=cons
                )


# print the Stocks and Weights into a manageable pd.DataFrame to be easier to read and export
def print_optimal_portfolio_dataframe(optimum, returns):
    # first create a variable to be passed into the new dataframe
    weights = optimum['x']
    # create the new dataframe with index = stocks
    optimal_portfolio_weights_df = pd.DataFrame({'Weights %': weights}, index=stocks)
    
    # create another dataframe that holds the metrics we are tracking for our portfolio
    headers = ['Expected Returns', 'Expected Volatility', 'Expected Sharpe Ratio']
    stats = statistics(optimum['x'].round(3), returns)
    metrics = pd.DataFrame({"Metrics": stats}, index=headers)
    
    print(metrics)
    # the weights are ordered in the same order as the stocks from above so they will print side by side
    print(optimal_portfolio_weights_df)


def show_optimal_portfolio(opt, rets, portfolio_rets, portfolio_vols):
    plt.figure(figsize=(20,10))
    plt.style.use(['dark_background'])
    plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets/portfolio_vols, marker='o')
    plt.grid(True)
    plt.rcParams.update({'font.size': 18})
    plt.title(f"Modern Portfolio Theory for {stocks}")
    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(opt['x'], rets)[1], statistics(opt['x'], rets)[0], 'r*', markersize=20.0)


def clean_df_monte_carlo(dataset, daily_returns):
    # bring in dataset and add multiindex column name 'close'
    dataset.columns = pd.MultiIndex.from_product([dataset.columns, ['close']])

    # bring in log_daily_returns and add multiindex column name 'daily_returns'
    daily_returns.columns = pd.MultiIndex.from_product([daily_returns.columns, ['daily_return']])

    # join the 2 tables together
    joined_df_columns = pd.concat(
        [dataset, daily_returns],
        axis='columns',
        join='inner'
    )

    # sort the columns by ticker symbol
    joined_df_columns.sort_index(axis=1, level=0, inplace=True)

    return pd.DataFrame(joined_df_columns)


def monte_carlo(dataset, optimum, investment):
    num_trading_days = 252
    # Configure the Monte Carlo simulation to forecast 30 years cumulative returns
    # The weights should be split 40% to AGG and 60% to SPY.
    # Run 500 samples.
    weights = optimum['x']

    optimal_portfolio_weights_df = pd.DataFrame({'Weights %': weights}, index=stocks)
    # dataset.columns = pd.MultiIndex.from_product([['close'], dataset.columns])

    MC_Stocks = MCSimulation(
        portfolio_data= dataset, 
        weights=weights,
        num_simulation=500,
        num_trading_days=num_trading_days
    )

    # Review the simulation input data
    MC_Stocks.calc_cumulative_return()

    mc_stock_tbl = MC_Stocks.summarize_cumulative_return()
    
    print(mc_stock_tbl)

    mc_ci_lower = round(mc_stock_tbl[8]*investment,2)
    mc_ci_upper = round(mc_stock_tbl[9]*investment,2)

    print(f"There is a 95% chance that an initial investment of ${investment} in the portfolio"
      f" over the next {round(num_trading_days / 252)} years will end within in the range of"
      f" ${mc_ci_lower} ({round(((mc_ci_lower - investment) / investment) * 100,2)}%) and ${mc_ci_upper} ({round(((mc_ci_upper - investment) / investment) * 100,2)}%).")

    return MC_Stocks


# in order to get both plots to show we had to create a separate function for each plot
# and pass the MC_Stocks dataframe in as a parameter
# ultimately we had to use "plt.show()" in order for the plots to populate individually
def mc_line_plot(MC_Stocks):
    MC_Stocks.plot_simulation()
    plt.show()

# mc_line_plot(MC_Stocks)


# in order to get both plots to show we had to create a separate function for each plot
# and pass the MC_Stocks dataframe in as a parameter
# ultimately we had to use "plt.show()" in order for the plots to populate individually
def mc_dist_plot(MC_Stocks):
    MC_Stocks.plot_distribution()
    plt.show()

# mc_dist_plot(MC_Stocks)


################################################################################################################
# # TESTING PHASE FOR-LOOP TO ADD SYMBOLS INTO SECTORS_1
# def stocks_in_sector(sectors_1, sectors_2, sectors_3):
#     csvpath = Path("./resources/stock_industry_marketcap.csv")
#     stocks = []
#     with open(csvpath, newline='') as csvfile:
#         rows = csv.reader(csvfile)
#         header = next(rows)
#         for row in rows:
#             gics_sector = float(rows[1])
#             symbol = float(rows[0])
#             marketcap = int(rows[2]).set_index("Market_Cap").sort_values(by="Market_Cap", ascending=False).iloc[0:5]
#             stocks = {
#                 # "GICS Sector": gics_sector,
#                 "Symbol":symbol,
#                 "Market_Cap":marketcap
#             }
#             if gics_sector == sectors_1:
#                 symbol.append(stocks)
#             if gics_sector == sectors_2:
#                 symbol.append(stocks)
#             if gics_sector == sectors_3:
#                 symbol.append(stocks)
#             return stocks
################################################################################################################

# def sector_interest_list()

# def initial_investment()


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

    # STEP 4: inputs top 5 stocks by marketcap into sector_interest
    # stocks_in_sector(sectors_1, sectors_2, sectors_3)

    # list of stocks as variable to pass to markowitz model

#################################################################################################################
# Markowitz Model Code:

    # value as initial investment
    # this is a parameter passed from questionary
    investment = 20000

    # these are variables selected by user and passed to the "download_data()" function
    stocks = ['AAPL', 'AMZN', 'GOOG', 'TSLA']

    # download_data() returns a dataframe called "dataset" that will be passed to the following functions:
    # calculate_log_return(), show_data(), calculate_return(), clean_df_monte_carlo()
    dataset = download_data(stocks)
    
    # calculate_log_return() takes the dataset variable and creates the log returns to the following functions:
    # generate_portfolio(), optimize_portfolio(), print_optimal_portfolio_dataframe(), show_optimal_portfolio()
    # calculate_log_return() is used to NORMALIZE the dataset
    log_daily_returns = calculate_log_return(dataset)

    # generate_portfolio() takes the log_daily_returns variable created by the calculate_log_return() function
    # from this function it will create the following lists as variables to be passed to further functions:
    # Variables : portfolio_weights, means, risk
    # passed to optimize_portfolio(), show_optimal_portfolio()
    portfolio_weights, means, risks = generate_portfolios(log_daily_returns)

    # optimize_portfolio() takes the portfolio_weights variable from generate_portfolios() 
    # and the log_daily_returns from calculate_log_return()
    # this function will return a variable named "optimum" which are the optimum weights for the selected stocks
    # this variable will be passed to the following down range functions:
    # show_optimal_portfolio(), monte_carlo()
    optimum = optimize_portfolio(portfolio_weights, log_daily_returns)

    # this function prints the metrics and weights of the portfolio for better clarity
    print_optimal_portfolio_dataframe(optimum, log_daily_returns)

    # this function graphs the simulation to generate the optimum weights and places a red star on the weights selected
    show_optimal_portfolio(optimum, log_daily_returns, means, risks)

    # this function returns a graph of historical price action based on 10 years of data
    show_data(dataset)

    # calculate_return() take the dataset as a parameter to calculate the standard returns to pass to the cleaned_df_monte_carlo()
    daily_return = calculate_return(dataset)

    # clean_df_monte_carlo() takes 2 dataframes (dataset, daily_returns) and combines them together to be passed to the monte_carlo()
    clean_df_monte_carlo = clean_df_monte_carlo(dataset, daily_return)

    # monte_carlo() runs the simulation to project the 95% confidence level of the value of the portfolio based on weight allocations
    # it returns a variable of MC_Stocks to pass to the plot functions down range
    MC_Stocks = monte_carlo(clean_df_monte_carlo, optimum, investment)

    # this plots the monte_carlo() simulation
    mc_line_plot(MC_Stocks)

    # this plots the 95% confidence levels of the monte_carlo()
    mc_dist_plot(MC_Stocks)

#################################################################################################################

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
