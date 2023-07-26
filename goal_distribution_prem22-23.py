import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Player_Shooting_22-23_prem - Sheet1.csv', header=[0, 1])
df.columns = df.columns.droplevel(0)
stats = df[['Player', 'Pos', 'Gls', 'Sh', 'SoT', 'xG']]

# Filter the data for multiple positions (e.g., forwards 'FW' and midfielders 'MF')
target_positions = ['FW', 'FW,MF', 'MF,FW', 'MF']
forwards_df = stats[stats['Pos'].isin(target_positions)]

# Convert the 'Gls' column to numeric data (if it contains any non-numeric values)
forwards_df['Gls'] = pd.to_numeric(forwards_df['Gls'], errors='coerce')

# Drop any rows with missing or non-numeric goal values
forwards_df = forwards_df.dropna(subset=['Gls'])

# Group by 'Player' and sum the values for each player
forwards_df = forwards_df.groupby('Player', as_index=False).sum()
print(forwards_df)

# Extract the 'Goals' column from the filtered DataFrame
goals_data = forwards_df['Gls']

# Get the highest value to set the range of x-axis
max_goals = goals_data.max()

# Create a histogram using the 'Goals' column
plt.hist(goals_data, bins=range(0, max_goals + 2), edgecolor='black')  # +2 to include the highest value

# Customize the plot
plt.xlabel('Goals Scored')
plt.ylabel('Number of Players')
plt.title('Distribution of Goals Scored by Forwards in the Premier League')
plt.grid(False)

# Show the histogram
plt.show()
