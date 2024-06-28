from investment_analysis import InvestmentAnalysis
from gpt4o_analyst import analyze_chart
import matplotlib.pyplot as plt 

#analysis = InvestmentAnalysis(['AAPL', 'GOOGL', 'MSFT'])

# Assuming you have a method like this that creates the plot
#analysis.plot_price_evolution()

ai_analyst = analyze_chart("screenshots/price_evolution-1719575123.3182921.png")

print(ai_analyst)