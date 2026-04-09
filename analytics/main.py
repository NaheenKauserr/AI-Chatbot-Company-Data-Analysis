from analysis import RetailDataAnalyzer
from insights import generate_ai_insights
from my_recommendations import generate_smart_recommendations

# Initialize analyzer
analyzer = RetailDataAnalyzer("C:/Users/HP/OneDrive/Desktop/AI-Chatbot-Company-Data-Analysis/dashboard/SALES_DATA_SETT.csv"
)

# Run base analysis
results = analyzer.run_complete_analysis()

# Generate insights & recommendations
insights = generate_ai_insights(results['kpis'])
recommendations = generate_smart_recommendations(results['kpis'])

# Print results
print("\n===== AI INSIGHTS =====")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

print("\n===== RECOMMENDATIONS =====")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")