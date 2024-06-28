import sys
from investment_analysis import InvestmentAnalysis

def print_menu():
    print("\nInvestment Analysis Menu:")
    print("1. Set Investment Policy Statement")
    print("2. View Summary Statistics")
    print("3. View Descriptive Statistics")
    print("4. View Additional Metrics")
    print("5. View Capital Allocation Lines")
    print("6. Input News Impact")
    print("7. View CAPM Metrics")
    print("8. Perform Stock Selection")
    print("9. Perform Portfolio Optimization")
    print("0. Exit")

def main():
    stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    analysis = InvestmentAnalysis(stocks)
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ")
        
        if choice == '0':
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        elif choice == '1':
            p_evolution = analysis.plot_price_evolution()
            print("Price Evolution:", p_evolution)
        elif choice == '2':
            analysis.summary_statistics()
        elif choice == '3':
            analysis.descriptive_statistics()
        elif choice == '4':
            analysis.additional_metrics()
        elif choice == '5':
            analysis.capital_allocation_lines()
        elif choice == '6':
            analysis.news_impact()
        elif choice == '7':
            analysis.capm_metrics()
        elif choice == '8':
            analysis.stock_selection()
        elif choice == '9':
            analysis.portfolio_optimization()
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
    