import numpy as np
import questionary
from sqlalchemy import log
# import yahoo finance to pull stock data
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization
# bringing in these libraries in order to use a dynamic date selection - see sub_years
import datetime as dt
from datetime import date
from CAPM import (CAPM, risk_free_rate)
from workflow.MCForecastTools import MCSimulation
from workflow.Markowitz_Model import (
    download_data,
    calculate_log_return,
    generate_portfolios,
    mc_invest_print,
    optimize_portfolio,
    print_optimal_portfolio_dataframe,
    show_optimal_portfolio,
    show_data,
    calculate_return,
    clean_df_monte_carlo,
    monte_carlo,
    mc_line_plot,
    mc_dist_plot,
    start_end,
    capm,
    mc_invest_print
)

from app import (
    sector_interest,
    investment_question,
    generate_tickers
)

from sector_return import (
    sector_return
)



def build_portfolio():
    today = date.today()



    start_date, end_date = start_end(today)

    # market interest rate
    # risk_free_rate = 0.05

    # we will consider monthly returns - and we want to calculate the annula return
    months_in_year = 12

    sectors = sector_return()

    # sectors_1, sectors_2, sectors_3=sectors()

    sectors_selected = sector_interest(sectors)

    stocks = generate_tickers(sectors_selected)

    # value as initial investment
    # this is a parameter passed from questionary
    investment = investment_question()

    # these are variables selected by user and passed to the "download_data()" function
    # stocks  = ['AAPL', 'AMZN', 'GOOG', 'TSLA'] #stock_generator(sectors_1, sectors_2, sectors_3)

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
    portfolio_weights, means, risks = generate_portfolios(stocks, log_daily_returns)

    # optimize_portfolio() takes the portfolio_weights variable from generate_portfolios() 
    # and the log_daily_returns from calculate_log_return()
    # this function will return a variable named "optimum" which are the optimum weights for the selected stocks
    # this variable will be passed to the following down range functions:
    # show_optimal_portfolio(), monte_carlo()
    optimum = optimize_portfolio(stocks, portfolio_weights, log_daily_returns)

    # show_mean_variance(log_daily_returns, optimum)
    # print_optimum(optimum, log_daily_returns)
    # this function prints the metrics and weights of the portfolio for better clarity
    metrics, optimal_portfolio_weights_df = print_optimal_portfolio_dataframe(stocks, optimum, log_daily_returns)

    # calculate_return() take the dataset as a parameter to calculate the standard returns to pass to the cleaned_df_monte_carlo()
    daily_return = calculate_return(dataset)

    # clean_df_monte_carlo() takes 2 dataframes (dataset, daily_returns) and combines them together to be passed to the monte_carlo()
    clean_df_mc = clean_df_monte_carlo(dataset, daily_return)

    # monte_carlo() runs the simulation to project the 95% confidence level of the value of the portfolio based on weight allocations
    # it returns a variable of MC_Stocks to pass to the plot functions down range
    MC_Stocks, mc_stock_tbl, mc_ci_upper, mc_ci_lower = monte_carlo(stocks, clean_df_mc, optimum, investment)

    risk_free_rate_1 = risk_free_rate()

    weights = optimum['x']
    # print all of the data to show metrics
    print(capm(stocks, start_date, end_date, risk_free_rate_1, weights))

    print(metrics)

    print(optimal_portfolio_weights_df)

    print(mc_stock_tbl)

    mc_invest_print(investment, mc_ci_upper, mc_ci_lower)

    # illustrate data
    # this function graphs the simulation to generate the optimum weights and places a red star on the weights selected
    print(show_optimal_portfolio(optimum, log_daily_returns, means, risks, sectors_selected))

    # this function returns a graph of historical price action based on 10 years of data
    print(show_data(dataset, start_date, end_date))

    # this plots the monte_carlo() simulation
    print(mc_line_plot(MC_Stocks))

    # this plots the 95% confidence levels of the monte_carlo()
    print(mc_dist_plot(MC_Stocks))

    # print(capm(stocks, start_date, end_date))

    # print(optimal_portfolio_weights_df)

    # print(mc_stock_tbl)

    # print(investment_return)

    # print(metrics)



    run_again = "Would you like to build another portfolio?"
    continue_running = questionary.select(run_again, choices=['y', 'n']).ask()

    return continue_running



if __name__ == '__main__':
    running = True

    while running:
        continue_running = build_portfolio()
        if continue_running == 'y':
            running = True
        else:
            running = False