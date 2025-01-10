import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'results_combatfootage.csv'
data = pd.read_csv(file_path)

# Rename columns for consistency
data.rename(columns={"label": "Sentiment"}, inplace=True)

# Calculate percentages
total_entries = len(data)
positive_count = len(data[data['Sentiment'] == 'POSITIVE'])
positive_percentage = (positive_count / total_entries) * 100
negative_percentage = 100 - positive_percentage

# Data for the bar chart
sentiment_data = {
    'Sentiment': ['Positive', 'Negative'],
    'Percentage': [positive_percentage, negative_percentage]
}
sentiment_df = pd.DataFrame(sentiment_data)

# Plot the bar chart
plt.figure(figsize=(6, 4))
bars = plt.bar(sentiment_df['Sentiment'], sentiment_df['Percentage'], color=['green', 'firebrick'])

# Add horizontal lines and percentage labels
for bar in bars:
    height = bar.get_height()
    plt.axhline(y=height, color='gray', linestyle='--', alpha=0.7)  # Horizontal line
    plt.text(bar.get_x() + bar.get_width() / 2, height + 2, f'{height:.1f}%', ha='center', fontsize=10)  # Percentage label

# Chart formatting
plt.xlabel('Sentiment')
plt.ylabel('Percentage')
plt.title('Sentiment Split in r/combatfootage')
plt.ylim(0, 100)  # Limit y-axis to 0-100 for percentage scale
plt.show()
