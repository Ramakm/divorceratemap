import pandas as pd
import folium
import geopandas
import numpy as np

url = 'https://en.wikipedia.org/wiki/Divorce_demography'
tables = pd.read_html(url)

table = tables[0]
table.columns = table.columns.droplevel(0)

table['Country'] = table.apply(lambda row: row['Country/region'].split(' (')[0] if type(row['Country/region']) == str else row['Country/region'], axis=1)

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world = world.replace('United States of America', 'United States')

table = world.merge(table, how="left", left_on=['name'], right_on=['Country'])

def is_float(str):
    try:
        float(str)
        return True
    except:
        return False

index = 'Divorce_float'
table[index] = table.apply(lambda row: float(row['Percent']) if is_float(row['Percent']) else np.nan, axis=1)

table = table.dropna(subset=[index])

bins_data = pd.qcut(table[index], 9).value_counts(sort=False)
print(bins_data)

bins = [0]
for i in range(9):
    bins.append(int(round(bins_data.index.values[i].right)))
bins[9] = 100

# Create a map
my_map = folium.Map()

folium.Choropleth(
    geo_data=table,
    name='choropleth',
    data=table,
    columns=['Country', index],
    key_on='feature.properties.name',
    fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=index,
    threshold_scale=bins
).add_to(my_map)
my_map.save('divorse_rates.html')
