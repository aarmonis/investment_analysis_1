import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class StockData:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()
        self.log_returns = self.calculate_log_returns()
    
    def download_data(self):
        data = {}
        for ticker in self.tickers:
            stock_data = yf.download(ticker, start= self.start_date, end = self.end_date)
            data[ticker] = stock_data
        return data
    
    def calculate_log_returns(self):
        log_returns = {}
        for ticker, data in self.data.items():
            log_returns[ticker] = (np.log(data['Close']) - np.log(data['Close'].shift(1))).dropna()
        return log_returns
        
            
    
    def plot_prices(self):
        for ticker in self.tickers:
            self.data[ticker]['Close'].plot(title = f"{ticker} Price Evolution", figsize = (10,6))
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.show()  # Ensure the plot is displayed
            
    def plot_log_returns(self):
        for ticker in self.tickers:
            self.log_returns[ticker].plot(title=f"{ticker} Log Returns", figsize=(10, 6))
            plt.xlabel("Date")
            plt.ylabel("Log Returns")
            plt.show()
        
    def compute_statistics(self):
        stats = {}
        for ticker, log_returns in self.log_returns.items():
            stats[ticker] = log_returns.describe()
        return stats
    
    def compute_correlation_covariance(self):
        log_returns_df = pd.DataFrame(self.log_returns)
        correlation = log_returns_df.corr()
        covariance = log_returns_df.cov()
        return correlation, covariance