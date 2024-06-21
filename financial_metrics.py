import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class FinancialMetrics:
    def __init__(self, stock_data,risk_free_rate=0.01):
        self.stock_data = stock_data
        self.log_returns = pd.DataFrame(stock_data.log_returns)
        self.market_returns = stock_data.market_log_returns
        self.risk_free_rate = risk_free_rate
        

    def compute_alpha_beta_rsquare(self):
        # Implement the alpha, beta, and R-square calculation
        metrics = {}
        for ticker in self.log_returns.columns:
            y = self.log_returns[ticker]
            X = self.market_returns.dropna()
            X = X.values.reshape(-1,1)
            
            model = LinearRegression().fit(X,y)
            alpha = model.intercept_
            beta = model.coef_[0]
            r_squared = model.score(X,y)
            metrics[ticker] = {'alpha': alpha, 'beta': beta, "r_squared": r_squared}
        return metrics

    def compute_capm_parameters(self):
        metrics = {}
        for ticker in self.log_returns.columns:
            y = self.log_returns[ticker] - self.risk_free_rate / 252
            X = self.market_returns.dropna() - self.risk_free_rate / 252
            X = X.values.reshape(-1,1)
            model = LinearRegression().fit(X,y)
            alpha = model.intercept_
            beta = model.coef_[0]
            r_squared = model.score(X,y)
            metrics[ticker] = {'alpha': alpha, 'beta': beta, "r_squared": r_squared}
        return metrics
    def plot_cal(self):
        # Implement the Capital Allocation Line plotting
        pass

    def compute_efficient_frontier(self):
        # Implement the efficient frontier calculation and plotting
        pass
