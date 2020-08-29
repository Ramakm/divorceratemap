Step 1: Get the data you want to correlate
As an example, let’s assume you get the idea that there might be a correlation between GDP per capita, Social Progress Index (SPI), and Human Development Index (HDI), but is not sure whether SPI or HDI is closets correlated to GDP per capita.

Luckily, you have pandas to the rescue.

As the data is in three pages, you need to collect it by separately and merge it later. First, let us collect the data and inspect it.

The GDP per capita is located in the table on wikipedia presented in the picture below.

Image 1 refer:

Step 2: Clean and merge the data into one DataFrame
If we first inspect the data from the GDP per capita.
    Rank                       Country/Territory     US$
0      1                           Monaco (2018)  185741
1      2                    Liechtenstein (2017)  173356
2      3                              Luxembourg  114705
3      —                                   Macau   84096
4      4                             Switzerland   81994
5      5                                 Ireland   78661
6      6                                  Norway   75420
7      7                                 Iceland   66945

import pandas as pd
import numpy as np


pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)


# The URL we will read our data from
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita'
# read_html returns a list of tables from the URL
tables = pd.read_html(url)

# The data is in table 3
table = tables[3]

# We need to clean the years in parenthesis from the country/territory field
table['Country'] = table.apply(lambda row: row['Country/Territory'].split(' (')[0], axis=1)
# We do not need the Rank and Country/Territory for more data
table = table.drop(['Rank', 'Country/Territory'], axis=1)

url = 'https://en.wikipedia.org/wiki/Social_Progress_Index'
tables = pd.read_html(url)

merge_table = tables[1]
# The first level of the table can be dropped
merge_table.columns = merge_table.columns.droplevel(0)
# We do not need the Rank and Score.1 columns
merge_table = merge_table.drop(['Rank', 'Score.1'], axis=1)
# Need to rename the second column to SPI = Social Progress Index
merge_table.columns = ['Country', 'SPI']

# Ready to merge the tables
table = table.merge(merge_table, how="left", left_on=['Country'], right_on=['Country'])

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index'
tables = pd.read_html(url)Step 3: Calculate the correlations
This is where the DataFrames from pandas come strong. It can do the entire work for you with one call to corr().

The full code is given below.

