import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def sentiment_upvote_matrix(dataset1_path, dataset2_path):
    # Load the datasets
    dataset1 = pd.read_csv(dataset1_path)
    dataset2 = pd.read_csv(dataset2_path)

    # Rename columns for consistency
    dataset1.rename(columns={"label": "Sentiment"}, inplace=True)
    dataset2.rename(columns={"label": "Sentiment"}, inplace=True)

    # Function to calculate matrix data
    def calculate_matrix(data):
        total = len(data)
        
        # Sentiment and Upvote Group Percentages
        neg_sent_neg_upvotes = len(data[(data['Sentiment'] == 'NEGATIVE') & (data['Upvotes'] < 0)]) / total * 100
        neg_sent_pos_upvotes = len(data[(data['Sentiment'] == 'NEGATIVE') & (data['Upvotes'] >= 0)]) / total * 100
        pos_sent_neg_upvotes = len(data[(data['Sentiment'] == 'POSITIVE') & (data['Upvotes'] < 0)]) / total * 100
        pos_sent_pos_upvotes = len(data[(data['Sentiment'] == 'POSITIVE') & (data['Upvotes'] >= 0)]) / total * 100
        
        # Marginal Percentages
        positive_sentiment = len(data[data['Sentiment'] == 'POSITIVE']) / total * 100
        negative_sentiment = len(data[data['Sentiment'] == 'NEGATIVE']) / total * 100
        positive_upvotes = len(data[data['Upvotes'] >= 0]) / total * 100
        negative_upvotes = len(data[data['Upvotes'] < 0]) / total * 100
        
        return {
            'matrix': [
                [neg_sent_neg_upvotes, neg_sent_pos_upvotes],
                [pos_sent_neg_upvotes, pos_sent_pos_upvotes]
            ],
            'marginals': {
                'sentiment': [negative_sentiment, positive_sentiment],
                'upvotes': [negative_upvotes, positive_upvotes]
            }
        }

    # Calculate data for both datasets
    matrix1 = calculate_matrix(dataset1)
    matrix2 = calculate_matrix(dataset2)

    # Function to plot the matrix
    def plot_matrix(matrix_data, dataset_name):
        matrix = matrix_data['matrix']
        marginals = matrix_data['marginals']

        fig, ax = plt.subplots(figsize=(8, 6))

        # Create the main matrix
        cax = ax.matshow(matrix, cmap='Blues', alpha=0.8)

        # Annotate the main matrix
        for (i, j), val in np.ndenumerate(matrix):
            ax.text(j, i, f'{val:.1f}%', ha='center', va='center', color='black')

        # Add sentiment percentages with rotation
        ax.set_yticks([0, 1])
        ax.set_yticklabels([
            f'Negative Sentiment ({marginals["sentiment"][0]:.1f}%)',
            f'Positive Sentiment ({marginals["sentiment"][1]:.1f}%)'
        ])
        for tick in ax.get_yticklabels():
            tick.set_rotation(90)
            tick.set_verticalalignment('center')

        # Add upvote percentages
        ax.set_xticks([0, 1])
        ax.set_xticklabels([
            f'Negative Upvotes ({marginals["upvotes"][0]:.1f}%)',
            f'Positive Upvotes ({marginals["upvotes"][1]:.1f}%)'
        ])

        # Axis labels
        ax.xaxis.set_label_position('top')
        ax.set_xlabel('Upvotes')
        ax.set_ylabel('Sentiment')

        # Add a colorbar
        fig.colorbar(cax, label='Percentage')

        plt.title(f'Sentiment-Upvote Matrix for {dataset_name}')
        plt.show()

    # Plot for both datasets
    plot_matrix(matrix1, 'r/combatfootage')
    plot_matrix(matrix2, 'r/geopolitics')



dataset1_path = 'results_combatfootage.csv'  # Replace with actual file path
dataset2_path = 'results_geopolitics.csv'  # Replace with actual file path
sentiment_upvote_matrix(dataset1_path, dataset2_path)
