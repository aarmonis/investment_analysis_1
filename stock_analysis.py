import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from typing import List
import yfinance as yf

class StockAnalysis:
    def __init__(self, stocks: List[str]):
        self.stocks = stocks
        self.data, self.market_data, self.risk_free_rate = self.load_data()

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
            print(f"2-year return: {(data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100:.2f}%")

    def descriptive_statistics(self):
        for stock in self.stocks:
            print(f"\nDescriptive statistics for {stock}:")
            data = self.data[stock]
            print(f"Mean: {data.mean():.2f}")
            print(f"Median: {data.median():.2f}")
            print(f"Standard deviation: {data.std():.2f}")
            print(f"Skewness: {data.skew():.2f}")
            print(f"Kurtosis: {data.kurt():.2f}")

    def additional_metrics(self):
        corr_matrix = self.data[self.stocks].corr()
        cov_matrix = self.data[self.stocks].cov()
        print("\nCorrelation matrix:\n", corr_matrix)
        print("\nCovariance matrix:\n", cov_matrix)

        for stock in self.stocks:
            market_returns = self.market_data.pct_change().dropna()
            stock_returns = self.data[stock].pct_change().dropna()
            beta, alpha, r_value, _, _ = linregress(market_returns, stock_returns)
            r_squared = r_value ** 2
            print(f"\nMetrics for {stock}:")
            print(f"Alpha: {alpha:.2f}")
            print(f"Beta: {beta:.2f}")
            print(f"R-squared: {r_squared:.2f}")

    def capital_allocation_lines(self):
        plt.figure(figsize=(10, 6))
        for stock in self.stocks:
            stock_returns = self.data[stock].pct_change().dropna()
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
            market_returns = self.market_data.pct_change().dropna()
            stock_returns = self.data[stock].pct_change().dropna()
            beta, alpha, r_value, _, _ = linregress(market_returns, stock_returns)
            r_squared = r_value ** 2
            print(f"\nCAPM metrics for {stock}:")
            print(f"Alpha: {alpha:.2f}")
            print(f"Beta: {beta:.2f}")
            print(f"R-squared: {r_squared:.2f}")
        
    def stock_selection(self):
        selected_stock = input("If you would choose one of these stocks, enter its ticker symbol: ")
        stock_returns = self.data[selected_stock].pct_change().dropna()
        market_returns = self.data[self.market_index].pct_change().dropna()
        stock_return = (1 + stock_returns).prod() - 1
        market_return = (1 + market_returns).prod() - 1
        print(f"\nSummary for {selected_stock}:")
        print(f"Your overall return from the stock: {stock_return * 100:.2f}%")
        print(f"Market return: {market_return * 100:.2f}%")

    def portfolio_optimization(self):
        stock_returns = self.data[self.stocks].pct_change().dropna()
        mean_returns = stock_returns.mean() * 252  # Annualized
        cov_matrix = stock_returns.cov() * 252  # Annualized

        plt.figure(figsize=(10, 6))
        portfolio_weights = []
        portfolio_returns = []
        portfolio_risks = []

        for weight1 in np.linspace(0, 1, 21):
            for weight2 in np.linspace(0, 1 - weight1, 21):
                for weight3 in np.linspace(0, 1 - weight1 - weight2, 21):
                    weight4 = 1 - weight1 - weight2 - weight3
                    weights = [weight1, weight2, weight3, weight4]
                    portfolio_return = np.dot(mean_returns, weights)
                    portfolio_risk = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
                    portfolio_weights.append(weights)
                    portfolio_returns.append(portfolio_return)
                    portfolio_risks.append(portfolio_risk)

        plt.scatter(portfolio_risks, portfolio_returns, c='r', marker='o')
        plt.xlabel('Risk (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.show()

        optimal_index = np.argmax(np.array(portfolio_returns) / np.array(portfolio_risks))
        optimal_return = portfolio_returns[optimal_index]
        optimal_risk = portfolio_risks[optimal_index]
        optimal_weights = portfolio_weights[optimal_index]

        print(f"\nOptimal portfolio allocation:")
        print(f"Expected return: {optimal_return:.2f}")
        print(f"Risk (Standard Deviation): {optimal_risk:.2f}")
        print(f"Optimal weights: {optimal_weights}")

if __name__ == '__main__':
    stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']

    analysis = StockAnalysis(stocks)

    #print("Investment Policy Statement:")
    #ips = analysis.investment_policy_statement()
    #print(ips)

    #print("\nSummary Statistics:")
    #analysis.summary_statistics()

    #print("\nDescriptive Statistics:")
    #analysis.descriptive_statistics()

    #print("\nAdditional Metrics:")
    #analysis.additional_metrics()

    #print("\nCapital Allocation Lines:")
    #analysis.capital_allocation_lines()

    #print("\nNews Impact:")
    #analysis.news_impact()

    #print("\nCAPM Metrics:")
    analysis.capm_metrics()

    #print("\nStock Selection:")
    #analysis.stock_selection()

    print("\nPortfolio Optimization:")
    analysis.portfolio_optimization()