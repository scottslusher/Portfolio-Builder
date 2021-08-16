import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import questionary
import json
import requests
from dotenv import load_dotenv
import os
from sector_return import (
    sector_return
)

from app import (
    sector_interest,
    generate_tickers
)

today = date.today()

# # once we have todays date we can run a formula to replace the year output from the date.today() with whatever timeframe we enter
# # in our program we will set this input at 10 years
def sub_years(years):
    today = date.today()
    
    try:
        return today.replace(year = today.year - years)
    except ValueError:
        return today + (date(today.year + years, 1, 1) - date(today.year, 1, 1))


def start_end(today):
    # historical data - define START and END dates
    # to calculate the start_date we must use the sub_years function defined above to get today's date and subtract 10 years
    # then using the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance
    start_date = sub_years(10).strftime('%Y-%m-%d')

    # for the end_date we just have to reformat the today variable with the .strftime('%Y-%m-%d') we format it so that it can be passed to yahoo finance 
    end_date = today.strftime('%Y-%m-%d')

    return start_date, end_date 

# market interest rate
# risk_free_rate = 0.05
# Pulls latest daily 1 year T-Bill for risk free rate.
def risk_free_rate():
    load_dotenv()
    quandl_api_key = os.getenv("QUANDL_API_KEY")
    request_url = "https://www.quandl.com/api/v3/datasets/USTREASURY/BILLRATES.json?api_key=7m6u44gzq_Ah45R24EPE"
    response = requests.get(request_url).json()
    risk_free_rate = response["dataset"]["data"][0][10]

    return risk_free_rate

# we will consider monthly returns - and we want to calculate the annula return
months_in_year = 12

class CAPM:
    def __init__(self, stocks, start_date, end_date, risk_free_rate, weights):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.risk_free_rate = risk_free_rate
        self.weights = weights

    def download_data(self):
        data = {}

        for stock in self.stocks:
            ticker = yf.download(stock, self.start_date, self.end_date)
            # Adjusted Closing Price takes into account factors such as dividends, stock splits, etc.
            # Adjusted Closing Price is a more accurate reflection of the stock's value
            data[stock] = ticker['Adj Close']

        return pd.DataFrame(data)

    def initialize(self):
        stocks_data = self.download_data()
        # clean the data so that there are no null values
        data_cleaned = stocks_data.fillna(stocks_data.rolling(6, min_periods=1).mean())
        data_cleaned = data_cleaned.dropna()
        # we use monthly returns ('M') instead of daily returns
        stocks_data = data_cleaned.resample('M').last()
        # slice off the S&P500
        sp500 = stocks_data.iloc[:,-1]
        sp500 = pd.DataFrame(sp500)

        sp500 = np.log(sp500 / sp500.shift(1))
        

        sp500['market_returns'] = sp500.sum(axis=1)

        # sp500['market_adjclose'] = sp500.sum(axis=1)
        
        
        # slice on the stocks
        stocks = stocks_data.iloc[:,:-1]
        stocks = np.log(stocks / stocks.shift(1))
        stocks = stocks.mul(self.weights)
        stocks = pd.DataFrame(stocks)

        stocks['sector_return'] = stocks.sum(axis=1)

        # sum the value of all stocks to create a sector value to create the daily returns
        # create a pandas dataframe to store stock information for analysis
        self.data = pd.DataFrame({'stock_weighted_return':stocks['sector_return'], 'market_returns':sp500['market_returns']})

        # add 2 columns for the s_returns and m_returns
        # logarithmic monthly returns
        # self.data[['stock_returns', 'market_returns']] = np.log(self.data[['stock_adjclose', 'market_adjclose']] / self.data[['stock_adjclose', 'market_adjclose']].shift(1))

        # remove NaN values
        self.data =  self.data[1:]

        # print(self.data)
        
    
    def calculate_beta(self):
        # covariance matrix: the diagonal items are teh variances
        # off diagonals are the covariances
        # the matrix is symmetric: cov[0,1] = cov[1,0]
        covariance_matrix = np.cov(self.data['stock_weighted_return'], self.data['market_returns'])
        # calculating beta according to the formula
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        # print("Beta from formula: ", beta)

    def regression(self):
        # using linear regression to fit a line to the data
        # [stock_returns, market_returns] - slope is the beta
        beta, alpha = np.polyfit(self.data['market_returns'], self.data['stock_weighted_return'], deg=1)
        # deg=1 linear line
        # deg=2 quadratic function to fit 
        # deg=3 cubic function to fit
        print(f"Beta from regression: {round(beta,4)}")
        # calculate the expected return according to the CAPM formula
        # we are after annual return (this is why multiply by 12)
        expected_return = self.risk_free_rate + beta * (self.data['market_returns'].mean() * months_in_year - self.risk_free_rate)

        print(f"Expected Weighted Return: {round(expected_return * 100,2)} %")
        self.plot_regression(alpha, beta)

        

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(20,10))
        axis.scatter(self.data['market_returns'], self.data['stock_weighted_return'], label='Portfolio Data Points')
        axis.plot(self.data['market_returns'], beta * self.data['market_returns'] + alpha, color='red', label='CAPM (S&P 500) Line')
        plt.title('Capital Asset Pricing Model - Correlation between Overall Market (S&P500) and Our Portfolio')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha $', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    sectors = sector_return()

    # sectors_1, sectors_2, sectors_3=sectors()

    sectors_selected = sector_interest(sectors)

    stocks = generate_tickers(sectors_selected)

    today = date.today()

    start_date, end_date = start_end(today)

    stocks.append('^GSPC')

    capm = CAPM(
        stocks,
        start_date,
        end_date
    )

    capm.initialize()
    capm.calculate_beta()
    capm.regression()