import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class StockData:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()
    
    def download_data(self):
        data = {}
        for ticker in self.tickers:
            stock_data = yf.download(ticker, start= self.start_date, end = self.end_date)
            data[ticker] = stock_data
        return data
    
    def plot_prices(self):
        for ticker in self.tickers:
            self.data[ticker]['Close'].plot(title = f"{ticker} Price Evolution", figsize = (10,6))
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.show()  # Ensure the plot is displayed
        
    def compute_statistics(self):
        pass
    
    def compute_correlation_covariance(self):
        pass