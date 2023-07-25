import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

names1880 = pd.read_csv('D:/Python/pydata-book-2nd-edition/datasets/babynames/yob1880.txt',
                        names=['name', 'sex', 'births'])

#These files only contain names with at least five occurrences in each year, so for sim‐
#plicity’s sake we can use the sum of the births column by sex as the total number of
#births in that year:

names1880.groupby('sex').births.sum()
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

#Since the dataset is split into files by year, one of the first things to do is to assemble
#all of the data into a single DataFrame and further to add a year field. You can do this
#using pandas.concat:

for year in years:
    path = 'D:/Python/pydata-book-2nd-edition/datasets/babynames/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)

# Concatenate everything into a single DataFrame

names = pd.concat(pieces, ignore_index=True)

#With this data in hand, we can already start aggregating the data at the year and sex
#level using groupby or pivot_table

###total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)

#Next, let’s insert a column prop with the fraction of babies given each name relative to
#the total number of births

def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group

#When performing a group operation like this, it’s often valuable to do a sanity check,
#like verifying that the prop column sums to 1 within all the groups

names = names.groupby(['year', 'sex']).apply(add_prop)
###print(names.groupby(['year', 'sex']).prop.sum())

#extract a subset of the data to facilitate further
#analysis: the top 1,000 names for each sex/year combination. This is yet another group operation

def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]
grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
#drop the group index, not needed
top1000.reset_index(inplace=True, drop=True)

#With the full dataset and Top 1,000 dataset in hand, we can start analyzing various
#naming trends of interest. Splitting the Top 1,000 names into the boy and girl por‐
#tions is easy to do first

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

#Simple time series, like the number of Johns or Marys for each year, can be plotted
#but require a bit of munging to be more useful. Let’s form a pivot table of the total
#number of births by year and name

total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

#Now, this can be plotted for a handful of names with DataFrame’s plot method

subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
###subset.plot(subplots=True, figsize=(12, 10), grid=False, title="Number of births per year")

#One explanation for the decrease in plots is that fewer parents are choosing common
#names for their children. This hypothesis can be explored and confirmed in the data.
#One measure is the proportion of births represented by the top 1,000 most popular
#names, which I aggregate and plot by year and sex

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

#Another interesting metric is the number of distinct names, taken in order of popularity
#from highest to lowest, in the top 50% of births. This number is a bit more tricky to compute.
#Let’s consider just the boy names from 2010

df = boys[boys.year == 2010]

#After sorting prop in descending order, we want to know how many of the most pop‐
#ular names it takes to reach 50%. You could write a for loop to do this, but a vector‐
#ized NumPy way is a bit more clever. Taking the cumulative sum, cumsum, of prop and
#then calling the method searchsorted returns the position in the cumulative sum at
#which 0.5 would need to be inserted to keep it in sorted order:

prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
#print(prop_cumsum.values.searchsorted(0.5))

#Since arrays are zero-indexed, adding 1 to this result gives you a result of 117. By con‐
#trast, in 1900 this number was much smaller:

df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()
in1900.values.searchsorted(0.5) + 1 #add one because of zero index

#You can now apply this operation to each year/sex combination, groupby those fields,
#and apply a function returning the count for each group:

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1
diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

#This resulting DataFrame diversity now has two time series, one for each sex, indexed by year

#diversity.plot(title="Number of popular names in top 50%")

#extract last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
letter_prop = subtable / subtable.sum()

fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
                      legend=False)

letter_prop = table / table.sum()
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
dny_ts.plot()

all_names = pd.Series(top1000.name.unique())
lesley_like = all_names[all_names.str.lower().str.contains('lesl')]
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
table = filtered.pivot_table('births', index='year', columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
table.plot(style={'M': 'k-', 'F': 'k--'})


#total_births.plot(title='Total births by sex and year')
plt.show()
