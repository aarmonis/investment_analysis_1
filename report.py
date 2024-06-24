import pandas as pd
import matplotlib.pyplot as plt

class Report:
    def __init__(self, stock_data, financial_metrics):
        self.stock_data = stock_data
        self.financial_metrics = financial_metrics

    def summary_statistics(self):
        statistics = self.stock_data.compute_statistics()
        for ticker, stats in statistics.items():
            print(f"\nSummary Statistics for {ticker}:")
            print(stats)

    def plot_cal(self):
        self.financial_metrics.plot_cal()

    def plot_efficient_frontier(self):
        self.financial_metrics.compute_efficient_frontier()

    def capm_summary(self):
        capm_metrics = self.financial_metrics.compute_capm_parameters()
        for ticker, metrics in capm_metrics.items():
            print(f"\nCAPM Parameters for {ticker}:")
            print(f"Alpha: {metrics['alpha']}")
            print(f"Beta: {metrics['beta']}")

    def sim_summary(self):
        sim_metrics = self.financial_metrics.compute_alpha_beta_rsquare()
        for ticker, metrics in sim_metrics.items():
            print(f"\nSingle Index Model Parameters for {ticker}:")
            print(f"Alpha: {metrics['alpha']}")
            print(f"Beta: {metrics['beta']}")
            print(f"R-squared: {metrics['r_squared']}")

    def optimal_portfolio_summary(self):
        max_sharpe_weights = self.financial_metrics.compute_efficient_frontier()
        print("\nWeights of the portfolio with the maximum Sharpe ratio:")
        for ticker, weight in zip(self.stock_data.tickers, max_sharpe_weights):
            print(f"{ticker}: {weight:.4f}")

    def generate_report(self):
        print("Generating Financial Analysis Report...\n")

        # Summary Statistics
        self.summary_statistics()

        # CAPM Summary
        self.capm_summary()

        # Single Index Model Summary
        self.sim_summary()

        # Plot CAL
        print("\nPlotting the Capital Allocation Line...")
        self.plot_cal()

        # Plot Efficient Frontier
        print("\nPlotting the Efficient Frontier...")
        self.plot_efficient_frontier()

        # Optimal Portfolio Summary
        self.optimal_portfolio_summary()

        print("\nReport generation complete.")
