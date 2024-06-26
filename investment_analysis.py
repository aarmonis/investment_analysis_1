import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from typing import List
import yfinance as yf

class InvestmentAnalysis:
    def __init__(self, stocks: List[str]):
        self.stocks = stocks
        self.data, self.market_data, self.risk_free_rate = self.load_data()
        self.log_returns = np.log(self.data / self.data.shift(1)).dropna()
        self.market_log_returns = np.log(self.market_data / self.market_data.shift(1)).dropna()

    def load_data(self):
        # Load the 2-year daily stock data
        start_date = pd.to_datetime('today') - pd.Timedelta(days=730)
        end_date = pd.to_datetime('today')

        stock_data = yf.download(self.stocks, start=start_date, end=end_date)['Adj Close']
        market_data = yf.download('^GSPC', start=start_date, end=end_date)['Adj Close']

        # Load the 3-month T-bill rate as a proxy for the risk-free rate
        risk_free_rate = yf.download('^IRX', start=start_date, end=end_date)['Adj Close'].mean() / 100

        return stock_data, market_data, risk_free_rate

    def investment_policy_statement(self) -> str:
        # Define your investment objective, constraints, and risk tolerance
        ips = input("Please enter your investment policy statement: ")
        return ips

    def summary_statistics(self):
        for stock in self.stocks:
            print(f"\nSummary statistics for {stock}:")
            data = self.data[stock]
            print(f"Price evolution:\n{data.plot(figsize=(10, 6))}")
            print(f"2-year return: {np.exp(self.log_returns[stock].sum()) - 1:.4f}")

    def descriptive_statistics(self):
        for stock in self.stocks:
            print(f"\nDescriptive statistics for {stock}:")
            log_returns = self.log_returns[stock]
            print(f"Mean: {log_returns.mean():.4f}")
            print(f"Median: {log_returns.median():.4f}")
            print(f"Standard deviation: {log_returns.std():.4f}")
            print(f"Skewness: {log_returns.skew():.4f}")
            print(f"Kurtosis: {log_returns.kurt():.4f}")

    def additional_metrics(self):
        corr_matrix = self.log_returns.corr()
        cov_matrix = self.log_returns.cov()
        print("\nCorrelation matrix:\n", corr_matrix)
        print("\nCovariance matrix:\n", cov_matrix)

        for stock in self.stocks:
            stock_returns = self.log_returns[stock]
            beta, alpha, r_value, _, _ = linregress(self.market_log_returns, stock_returns)
            r_squared = r_value ** 2
            print(f"\nMetrics for {stock}:")
            print(f"Alpha: {alpha:.4f}")
            print(f"Beta: {beta:.4f}")
            print(f"R-squared: {r_squared:.4f}")

    def capital_allocation_lines(self):
        plt.figure(figsize=(10, 6))
        for stock in self.stocks:
            stock_returns = self.log_returns[stock]
            stock_mean_return = stock_returns.mean() * 252  # Annualized
            stock_std = stock_returns.std() * np.sqrt(252)  # Annualized
            x = np.linspace(0, stock_std, 100)
            y = x * (stock_mean_return - self.risk_free_rate) / stock_std + self.risk_free_rate
            plt.plot(x, y, label=stock)
        plt.xlabel('Risk (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Capital Allocation Lines')
        plt.legend()
        plt.show()

    def news_impact(self):
        for stock in self.stocks:
            print(f"\nSignificant news for {stock} in the last 3 months:")
            news = input(f"Enter news for {stock}: ")
            print(f"News impact: {news}")

    def capm_metrics(self):
        for stock in self.stocks:
            stock_returns = self.log_returns[stock]
            beta, alpha, r_value, _, _ = linregress(self.market_log_returns, stock_returns)
            r_squared = r_value ** 2
            print(f"\nCAPM metrics for {stock}:")
            print(f"Alpha: {alpha:.4f}")
            print(f"Beta: {beta:.4f}")
            print(f"R-squared: {r_squared:.4f}")
        
    def stock_selection(self):
        selected_stock = input("If you would choose one of these stocks, enter its ticker symbol: ")
        stock_returns = self.log_returns[selected_stock]
        stock_return = np.exp(stock_returns.sum()) - 1
        market_return = np.exp(self.market_log_returns.sum()) - 1
        print(f"\nSummary for {selected_stock}:")
        print(f"Your overall return from the stock: {stock_return:.4f}")
        print(f"Market return: {market_return:.4f}")

    def portfolio_optimization(self, num_portfolios=10000):
        returns = self.log_returns.mean() * 252  # Annualized returns
        cov_matrix = self.log_returns.cov() * 252  # Annualized covariance matrix
        num_assets = len(returns)

        results = np.zeros((4, num_portfolios))
        weights_record = []

        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            
            portfolio_return = np.dot(weights, returns)
            portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_stddev
            
            results[0,i] = portfolio_return
            results[1,i] = portfolio_stddev
            results[2,i] = sharpe_ratio
            results[3,i] = np.max(weights)

        max_sharpe_idx = np.argmax(results[2])
        sdp, rp = results[1, max_sharpe_idx], results[0, max_sharpe_idx]
        max_sharpe_weights = weights_record[max_sharpe_idx]

        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o')
        ax.scatter(sdp, rp, c='red', marker='*', s=100, label='Max Sharpe Ratio')
        fig.colorbar(scatter, ax=ax, label='Sharpe Ratio')
        ax.set_xlabel('Volatility')
        ax.set_ylabel('Return')
        plt.title('Efficient Frontier')
        plt.legend()
        plt.show()

        print(f"\nOptimal portfolio allocation (Max Sharpe Ratio):")
        print(f"Expected return: {rp:.4f}")
        print(f"Volatility: {sdp:.4f}")
        print(f"Sharpe Ratio: {results[2, max_sharpe_idx]:.4f}")
        print("Optimal weights:")
        for stock, weight in zip(self.stocks, max_sharpe_weights):
            print(f"{stock}: {weight:.4f}")

        return max_sharpe_weights