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
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot risk-free rate
        ax.axhline(self.risk_free_rate, color='gray', linestyle='--', label='Risk-Free Rate')
        
        for ticker in self.log_returns.columns:
            log_returns = self.log_returns[ticker]
            
            # Calculate annualized expected return and standard deviation
            expected_return = log_returns.mean() * 252  # Annualize the expected return
            std_dev = log_returns.std() * np.sqrt(252)  # Annualize the standard deviation
            
            # Calculate Sharpe ratio
            sharpe_ratio = (expected_return - self.risk_free_rate) / std_dev
            
            # Plot the CAL
            cal_x = np.linspace(0, std_dev * 2, 100)
            cal_y = self.risk_free_rate + cal_x * sharpe_ratio
            
            ax.plot(cal_x, cal_y, label=f'{ticker} CAL (Sharpe Ratio: {sharpe_ratio:.2f})')
        
        ax.set_xlabel('Standard Deviation')
        ax.set_ylabel('Expected Return')
        ax.legend()
        plt.title('Capital Allocation Line')
        plt.show()

        
    def compute_efficient_frontier(self, num_portfolios=10000):
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
            results[3,i] = np.max(weights)  # Just an example to record weights

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

        return max_sharpe_weights

        
