import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Load the dataset
file_path = './data/results_combatfootage.csv'
data = pd.read_csv(file_path)

# Rename columns for consistency
data.rename(columns={"label": "Sentiment", "score": "Score"}, inplace=True)

# Apply signed log transformation to Upvotes
def signed_log_transform(value):
    return np.sign(value) * np.log1p(abs(value))

data['Upvotes_log'] = data['Upvotes'].apply(signed_log_transform)

# Split the data by sentiment
negative_data = data[data['Sentiment'] == 'NEGATIVE']
positive_data = data[data['Sentiment'] == 'POSITIVE']

# Function to reverse the signed log transformation
def inverse_signed_log_transform(value):
    return np.sign(value) * (np.expm1(abs(value)))

# Custom tick positions for true values
custom_ticks = [-1000, -100, -10, -1, 0, 1, 10, 100, 1000, 10000, 100000]
log_ticks = [signed_log_transform(tick) for tick in custom_ticks]

# Plot the distributions with a signed logarithmic x-axis
plt.figure(figsize=(10, 6))

# KDE Plot for NEGATIVE
sns.kdeplot(negative_data['Upvotes_log'], label='Negative Sentiment', color='blue', fill=True, alpha=0.5)

# KDE Plot for POSITIVE
sns.kdeplot(positive_data['Upvotes_log'], label='Positive Sentiment', color='green', fill=True, alpha=0.5)

# Set custom ticks and format them
plt.xticks(log_ticks, custom_ticks)
plt.xlabel('Upvotes (Signed Logarithmic Scale)')
plt.ylabel('Kernel Density Estimation')
plt.title('Upvote Distribution by Sentiment in r/combatfootage')
plt.legend()
plt.show()
