import pandas as pd
import matplotlib.pyplot as plt

def plot_positive_percentage(dataset1_path, dataset2_path):
    # Load the datasets
    dataset1 = pd.read_csv(dataset1_path)
    dataset2 = pd.read_csv(dataset2_path)

    # Rename columns for consistency
    dataset1.rename(columns={"label": "Sentiment"}, inplace=True)
    dataset2.rename(columns={"label": "Sentiment"}, inplace=True)

    # Calculate positive sentiment percentages
    total1 = len(dataset1)
    positive1 = len(dataset1[dataset1['Sentiment'] == 'POSITIVE'])
    positive_percentage1 = (positive1 / total1) * 100

    total2 = len(dataset2)
    positive2 = len(dataset2[dataset2['Sentiment'] == 'POSITIVE'])
    positive_percentage2 = (positive2 / total2) * 100

    # Data for the bar chart
    sentiment_data = {
        'Dataset': ['Dataset 1', 'Dataset 2'],
        'Positive Percentage': [positive_percentage1, positive_percentage2]
    }
    sentiment_df = pd.DataFrame(sentiment_data)

    # Plot the bar chart
    plt.figure(figsize=(6, 4))
    bars = plt.bar(sentiment_df['Dataset'], sentiment_df['Positive Percentage'], color=['blue', 'orange'])

    # Add horizontal lines and percentage labels
    for bar in bars:
        height = bar.get_height()
        plt.axhline(y=height, color='gray', linestyle='--', alpha=0.7)  # Horizontal line
        plt.text(bar.get_x() + bar.get_width() / 2, height + 2, f'{height:.1f}%', ha='center', fontsize=10)  # Percentage label

    # Chart formatting
    plt.xlabel('Dataset')
    plt.ylabel('Positive Sentiment Percentage')
    plt.title('Positive Sentiment Percentage in Two Datasets')
    plt.ylim(0, 100)  # Limit y-axis to 0-100 for percentage scale
    plt.show()

# Example usage
dataset1_path = 'results_geopolitics.csv'  # Replace with actual file path
dataset2_path = 'results_combatfootage.csv'  # Replace with actual file path
plot_positive_percentage(dataset1_path, dataset2_path)
