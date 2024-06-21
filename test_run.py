from stock_data import StockData

def main():
    tickers = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    start_date = "2022-01-01"
    end_date = "2024-01-01"
    
    stock_data = StockData(tickers, start_date, end_date)
    
    print("Plotting stock prices...")
    stock_data.plot_prices()
    
    
if __name__ == "__main__":
    main()
    