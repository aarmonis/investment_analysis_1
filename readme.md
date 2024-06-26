# Investment Analysis Tool

## Overview

This Investment Analysis Tool is a Python-based application that provides various financial analysis capabilities for a portfolio of stocks. It implements modern portfolio theory concepts and offers insights into stock performance, risk assessment, and portfolio optimization.

## Features

1. **Data Loading**: Fetches 2-year daily stock data, market data (S&P 500), and risk-free rate (3-month T-bill) using the yfinance library.

2. **Investment Policy Statement**: Allows users to input their investment objectives and constraints.

3. **Summary Statistics**: Displays price evolution and 2-year returns for each stock.

4. **Descriptive Statistics**: Calculates mean, median, standard deviation, skewness, and kurtosis for each stock's log returns.

5. **Additional Metrics**: Computes correlation and covariance matrices, as well as alpha, beta, and R-squared for each stock.

6. **Capital Allocation Lines**: Plots capital allocation lines for each stock.

7. **News Impact**: Allows users to input significant news affecting each stock.

8. **CAPM Metrics**: Calculates Capital Asset Pricing Model metrics for each stock.

9. **Stock Selection**: Compares the return of a selected stock to the market return.

10. **Portfolio Optimization**: Performs portfolio optimization using the efficient frontier method and visualizes the results.

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- scipy
- yfinance

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/investment-analysis-tool.git
   cd investment-analysis-tool
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:
   ```
   python main.py
   ```

2. Follow the on-screen menu to select different analysis options.

3. Input data as prompted (e.g., investment policy statement, news impacts).

4. View the results in the console and generated plots.

## File Structure

- `main.py`: The main script that runs the user interface.
- `investment_analysis.py`: Contains the `InvestmentAnalysis` class with all analysis methods.
- `requirements.txt`: Lists all Python dependencies.

## Notes

- This tool uses log returns for all calculations, which is more appropriate for financial analysis, especially when dealing with multi-period returns.
- The portfolio optimization method uses a Monte Carlo simulation to generate random portfolios and find the optimal allocation based on the Sharpe ratio.
- All visualizations are generated using matplotlib and displayed during the analysis.

## Limitations

- The tool assumes normally distributed returns and static correlations, which may not always hold in reality.
- It's based on historical data, which may not predict future performance.
- Transaction costs and taxes are not accounted for in the calculations.
- The tool assumes investors can lend and borrow at the risk-free rate.


## Contributing

Contributions to improve the tool are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
