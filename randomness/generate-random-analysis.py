import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data (assumes a CSV or similar)
# Columns: profile_id, label_desc, draw_schedule_id
df = pd.read_csv("winners.csv")

# Function to plot prize distribution per user for a specific draw
def plot_prize_distribution(draw_id):
    df_draw = df[df['draw_schedule_id'] == draw_id]

    # Count prize types per user
    grouped = df_draw.groupby(['profile_id', 'label_desc']).size().reset_index(name='count')

    # 1. Prize counts per user
    plt.figure(figsize=(12, 6))
    sns.histplot(data=grouped, x='count', bins=20, kde=True)
    plt.title(f'Distribution of Prize Type Counts per User for Draw {draw_id}')
    plt.xlabel('Number of Wins (per type)')
    plt.ylabel('Frequency')
    plt.show()

    # 2. Number of different prize types per user
    prize_per_user = df_draw.groupby('profile_id')['label_desc'].nunique().reset_index(name='unique_prizes')

    plt.figure(figsize=(10, 5))
    sns.histplot(prize_per_user['unique_prizes'], bins=20, kde=True, color='green')
    plt.title(f'Unique Prize Types per User in Draw {draw_id}')
    plt.xlabel('Unique Prize Types Won')
    plt.ylabel('Number of Users')
    plt.show()

    # 3. Total prizes per user
    total_prizes = df_draw['profile_id'].value_counts()

    plt.figure(figsize=(12, 5))
    sns.histplot(total_prizes, bins=30, color='orange')
    plt.title(f'Total Prizes per User in Draw {draw_id}')
    plt.xlabel('Total Prizes Won')
    plt.ylabel('Number of Users')
    plt.show()

    # 4. Heatmap: users vs prize types
    pivot = df_draw.pivot_table(index='profile_id', columns='label_desc', aggfunc='size', fill_value=0)

    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.5)
    plt.title(f'Prize Type Heatmap per User for Draw {draw_id}')
    plt.xlabel('Prize Type')
    plt.ylabel('User')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage for draw_schedule_id = 2
    plot_prize_distribution(2)
