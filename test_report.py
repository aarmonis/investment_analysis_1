from stock_data import StockData
from financial_metrics import FinancialMetrics
from report import Report
import yfinance as yf

def main():
    # Define the tickers, start date, and end date for testing
    tickers = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    market_ticker = "^GSPC"  # S&P 500 as market index
    start_date = "2022-01-01"
    end_date = "2024-01-01"

    # Initialize the StockData object
    stock_data = StockData(tickers, market_ticker, start_date, end_date)

    # Initialize the FinancialMetrics object
    financial_metrics = FinancialMetrics(stock_data)

    # Initialize the Report object
    report = Report(stock_data, financial_metrics)

    # Generate the report
    report.generate_report()

if __name__ == "__main__":
    main()
