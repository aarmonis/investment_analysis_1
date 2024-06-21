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
    
    #Download Market Data
    #market_data = yf.download(market_ticker, start=start_date, end=end_date)
    #market_returns = (np.log(market_data['Close']) - np.log(market_data['Close'].shift(1)))
    
    #Initialize FinancialMetrics object
    
    financial_metrics = FinancialMetrics(stock_data)
    
     # Compute alpha, beta, and R-squared using the Single Index Model
    print("Computing alpha, beta, and R-squared using the Single Index Model...")
    sim_metrics = financial_metrics.compute_alpha_beta_rsquare()
    for ticker, metrics in sim_metrics.items():
        print(f"\nSIM Metrics for {ticker}:")
        print(f"Alpha: {metrics['alpha']}")
        print(f"Beta: {metrics['beta']}")
        print(f"R-squared: {metrics['r_squared']}")
    
     # Compute CAPM parameters (alpha and beta)
    print("Computing CAPM parameters (alpha and beta)...")
    capm_metrics = financial_metrics.compute_capm_parameters()
    for ticker, metrics in capm_metrics.items():
        print(f"\nCAPM Parameters for {ticker}:")
        print(f"Alpha: {metrics['alpha']}")
        print(f"Beta: {metrics['beta']}")
        print(f"R-squared: {metrics['r_squared']}")
if __name__ == "__main__":
    main()
        
        