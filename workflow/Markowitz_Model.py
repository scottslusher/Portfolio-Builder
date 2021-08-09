import numpy as np
# import yahoo finance to pull stock and crypto data from
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization
# bringing in these libraries in order to use a dynamic date selection - see sub_years
import datetime as dt
from datetime import date
from workflow.MCForecastTools import MCSimulation
################################################################################################################
# MARKOWITZ MODEL:
# stocks = ['AAPL', 'AMZN', 'GOOG', 'TSLA']
# we want the user to focus on the assets they are wanting to analyze and not the amount of data the program is analyzing
# so in order to get the most relevant information we create a dynamic date range with a rolling 10 year window
# first we create a variable today and set it equal to the datetime libraries date.today() 
today = date.today()

# # once we have todays date we can run a formula to replace the year output from the date.today() with whatever timeframe we enter
# # in our program we will set this input at 10 years
def sub_years(today_date, years):
    try:
        return today_date.replace(year = today_date.year - years)
    except ValueError:
        return today_date + (date(today_date.year + years, 1, 1) - date(today_date.year, 1, 1))

# # historical data - define START and END dates
# # to calculate the start_date we must use the sub_years function defined above to get today's date and subtract 10 years
# # then using the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance
start_date = sub_years(today, 10).strftime('%Y-%m-%d')
# # for the end_date we just have to reformat the today variable with the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance 
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


def generate_portfolios(stocks, returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(num_portfolios):
        # w = np.random.random(len(stocks))
        w = np.random.random(len(stocks))
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
def optimize_portfolio(stocks, weights, returns):
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
def print_optimal_portfolio_dataframe(stocks, optimum, returns):
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


def show_optimal_portfolio(stocks, opt, rets, portfolio_rets, portfolio_vols):
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


def monte_carlo(stocks, dataset, optimum, investment):
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