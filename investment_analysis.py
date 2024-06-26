import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from typing import List
import yfinance as yf
import seaborn as sns
import os
import time


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
 

    def plot_and_save_all(self):
        # Ensure the screenshots directory exists
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        t = time.time()
        saved_files = []

        # 1. Price Evolution Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
        
        for stock in self.stocks:
            ax1.plot(self.data.index, self.data[stock], label=stock)
        
        ax1.set_title('Price Evolution of Stocks')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)

        normalized_data = self.data / self.data.iloc[0] * 100
        for stock in self.stocks:
            ax2.plot(normalized_data.index, normalized_data[stock], label=stock)
        
        ax2.set_title('Normalized Price Evolution (Starting from 100)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Normalized Price')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        price_evolution_filename = f"screenshots/price_evolution-{t}.png"
        plt.savefig(price_evolution_filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved_files.append(price_evolution_filename)

        # 2. Correlation Heatmap
        correlation_matrix = self.data.pct_change().corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title('Stock Price Movement Correlation Heatmap')
        correlation_filename = f"screenshots/correlation_heatmap-{t}.png"
        plt.savefig(correlation_filename, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(correlation_filename)

        # 3. Individual Stock Performance
        for stock in self.stocks:
            plt.figure(figsize=(10, 6))
            plt.plot(self.data.index, self.data[stock])
            plt.title(f'{stock} Price Evolution')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.grid(True)
            stock_filename = f"screenshots/{stock}_evolution-{t}.png"
            plt.savefig(stock_filename, dpi=300, bbox_inches='tight')
            plt.close()
            saved_files.append(stock_filename)

        print(f"All plots saved. Files created:")
        for file in saved_files:
            print(f"- {file}")

        return saved_files
        
            
    def plot_price_evolution(self):
        
        # Ensure the screenshots directory exists
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        t = time.time()
        saved_files = []
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
        
        # Plot 1: Price Evolution
        for stock in self.stocks:
            ax1.plot(self.data.index, self.data[stock], label=stock)
        
        ax1.set_title('Price Evolution of Stocks')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)

        # Plot 2: Normalized Price Evolution (Starting from 100)
        normalized_data = self.data / self.data.iloc[0] * 100
        for stock in self.stocks:
            ax2.plot(normalized_data.index, normalized_data[stock], label=stock)
        
        ax2.set_title('Normalized Price Evolution (Starting from 100)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Normalized Price')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()
        price_evolution_filename = f"screenshots/fix_price_evolution-{t}.png"
        plt.savefig(price_evolution_filename, dpi=300, bbox_inches='tight')
        saved_files.append(price_evolution_filename)

        # Calculate and print additional metrics
        print("\nPrice Evolution Metrics:")
        for stock in self.stocks:
            stock_data = self.data[stock]
            overall_return = (stock_data.iloc[-1] / stock_data.iloc[0] - 1) * 100
            max_price = stock_data.max()
            min_price = stock_data.min()
            current_price = stock_data.iloc[-1]
            drawdown = ((max_price - current_price) / max_price) * 100
            volatility = stock_data.pct_change().std() * (252 ** 0.5) * 100  # Annualized volatility

            print(f"\n{stock}:")
            print(f"  Overall Return: {overall_return:.2f}%")
            print(f"  Max Price: ${max_price:.2f}")
            print(f"  Min Price: ${min_price:.2f}")
            print(f"  Current Price: ${current_price:.2f}")
            print(f"  Drawdown from Peak: {drawdown:.2f}%")
            print(f"  Annualized Volatility: {volatility:.2f}%")

        # Calculate and print correlation matrix
        correlation_matrix = self.data.pct_change().corr()
        print("\nCorrelation Matrix:")
        print(correlation_matrix)

        # Plot correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title('Stock Price Movement Correlation Heatmap')
        plt.tight_layout()
        plt.show()
        
        return saved_files
        

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