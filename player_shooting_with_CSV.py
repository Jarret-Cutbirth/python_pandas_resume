import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

stats_shooting = pd.read_csv('stats_shooting.csv', header=[0, 1])
stats_shooting.columns = stats_shooting.columns.droplevel(0)
df = stats_shooting[['Player', '90s', 'Sh', 'SoT', 'Gls', 'xG']]

print(df)

# calculate mean regression for xG and goals
df['xG Reg'] = df['Gls'] - df['xG']
xg_reg_mean = df['xG Reg'].mean()

# calculate mean regression for shots and shots on target
df['Sh Reg'] = df['SoT'] - df['Sh']
sh_reg_mean = df['Sh Reg'].mean()

# plot xG vs goals using scatter plot with random color points
ax = sns.scatterplot(data=df, x='xG', y='Gls', hue='Player', palette='bright', legend=False)
# add regression line using regplot
sns.regplot(data=df, x='xG', y='Gls', color='black', scatter=False, ci=None)
plt.title("xG vs Goals for Premier League Players")
plt.xlabel("xG")
plt.ylabel("Goals")

# add labels for top 10 players
top_xg_players = df.nlargest(10, 'Gls')['Player']
for i, player in enumerate(top_xg_players):
    ax.text(df.loc[df['Player']==player, 'xG'] + 0.01, df.loc[df['Player']==player, 'Gls'] + 0.01, str(i+1)+". "+player)

plt.show()

# plot Sh vs SoT using scatter plot with random color points
sns.scatterplot(data=df, x='Sh', y='SoT', hue='Player', palette='bright', legend=False)
# add regression line and horizontal line using regplot
sns.regplot(data=df, x='Sh', y='SoT', color='black', scatter=False, ci=None)
plt.title("Shots vs Shots on Target for Premier League Players")
plt.xlabel("Shots")
plt.ylabel("Shots on Target")

# add labels for top 10 players
top_sh_players = df.nlargest(10, 'Gls')['Player']
for i, player in enumerate(top_sh_players):
    ax.text(df.loc[df['Player']==player, 'Sh'] + 0.01, df.loc[df['Player']==player, 'SoT'] + 0.01, str(i+1)+". "+player)

plt.show()

# display the final table sorted by xG regression
df = df.sort_values('xG Reg', ascending=False)
print(df)
print("xG Regression Mean:", xg_reg_mean)
print("Shots Regression Mean:", sh_reg_mean)
