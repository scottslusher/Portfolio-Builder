### WORKING ON THIS FILE, TESTING IF THIS IS WORTH DOING.

"""Industrials List

This file calculates the top 5 stocks in the the industrials list by marketcap

"""
import yfinance as yf

def top_5_industrial_stocks(industrials_sp500, sp500_df_wo_index, industrials_list):
    # list all stocks in the industrials sector of the SP500 
    industrials_sp500 = sp500_df_wo_index.loc["Industrials"]
    industrials_list = industrials_sp500["Symbol"].values.tolist()
        
def market_cap(industrials_list):

    market_cap = {}

    for stock in industrials_list:
        ticker = yf.Ticker(stock)
        market_cap[stock] = ticker.info['marketCap']
      
    # we want to return a sorted Pandas DataFrame based on market cap and filtered to the top 5
    # since the columns will originally be the ticker we us ".T" to transpose the table
    # then we use .sort_values to sort by the "first column" [0] and sort in decending order
    # then we only call the top 5 by using "[0:5]"
    # on average this takes 320 seconds (5 minutes 20 seconds) to run per sector
    return pd.DataFrame(market_cap, index=[0]).T.sort_values(by=[0], ascending=False)[0:5]
