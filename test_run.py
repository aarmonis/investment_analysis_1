from stock_data import StockData

def main():
    tickers = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    start_date = "2022-01-01"
    end_date = "2024-01-01"
    
    stock_data = StockData(tickers, start_date, end_date)
    
    print("Plotting stock prices...")
    #stock_data.plot_prices()
    
    print("Printing log returns...")
    #stock_data.plot_log_returns()
    
    print("Computing stats")
    stats = stock_data.compute_statistics()
    for ticker, stat in stats.items():
        print(f"\nStatistics for {ticker}:")
        print(stat)
    
     # Compute and print correlation and covariance
    print("Computing correlation and covariance...")
    correlation, covariance = stock_data.compute_correlation_covariance()
    print("\nCorrelation Matrix:")
    print(correlation)
    print("\nCovariance Matrix:")
    print(covariance)
    
    
if __name__ == "__main__":
    main()
    