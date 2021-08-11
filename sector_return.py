import pandas as pd
import sqlalchemy as sql
import yfinance as yf
from pathlib import Path

def sector_return():
    csvpath = Path("resources/stock_industry_marketcap.csv")
    sp500_csv = pd.read_csv(csvpath)
    sector = "GICS Sector"
    sp500_sectors = sp500_csv[sector].drop_duplicates().to_list()

    # Create a database connection string that links an in-memory database
    database_connection_string = 'sqlite:///stock_industry_top5.db'

    # Database connection object
    engine = sql.create_engine(database_connection_string)

    # Confirm the engine was created
    engine

    sector_returns = []

    for s in sp500_sectors:

        top5_1 = f"""
        SELECT Symbol, `GICS Sector`
        FROM stock_industry_marketcap
        WHERE `GICS Sector` = '{s}'
        ORDER BY Market_Cap DESC
        LIMIT 5
        """
        results_1 = engine.execute(top5_1)
        data_1 = pd.DataFrame(results_1)

        symbols = data_1[0].tolist()

        stock_data = yf.download(
            #tickers list or string as well
            tickers = symbols,

            # use "period" instead of start/end
            # valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            # (optional, default is "1mo")
            period = "1y",

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

        data_cleaned = stock_data.fillna(stock_data.rolling(6, min_periods=1).mean())
        data_cleaned = data_cleaned.dropna()

        sector_pct_change = data_cleaned.pct_change()

        sector_pct_change['sector_pct_change'] = sector_pct_change.mean(axis=1)
        
        sector_yearly_rtn = sector_pct_change['sector_pct_change'].sum()

        sector_returns.append(sector_yearly_rtn)

    # print(sp500_sectors)
    # print(sector_returns)

    annual_return_df = pd.DataFrame(
        {'Sectors':sp500_sectors,
        'Annual_Return':sector_returns}
        )

    annual_return_df.set_index('Sectors', inplace=True)
    annual_return_df = annual_return_df.sort_values(by='Annual_Return', ascending=False)

    print(annual_return_df)

    return sp500_sectors



if __name__ == "__main__":
    sector_return