from stock_data import StockData
from financial_metrics import FinancialMetrics
import yfinance as yf
import numpy as np

def main():
    # Define the tickers, start date, and end date for testing
    tickers = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    market_ticker = "^GSPC"  # S&P 500 as market index
    start_date = "2022-01-01"
    end_date = "2024-01-01"

    # Initialize the StockData object
    stock_data = StockData(tickers, market_ticker, start_date, end_date)

    # Initialize the FinancialMetrics object
    financial_metrics = FinancialMetrics(stock_data)
    
    #plot Capital Allocation Line
    print("Plotting the CAL...")
    #financial_metrics.plot_cal()
    
    print("Plotting Efficient Frontier...")
    financial_metrics.compute_efficient_frontier()
    
    
    
    
if __name__ == "__main__":
    main()