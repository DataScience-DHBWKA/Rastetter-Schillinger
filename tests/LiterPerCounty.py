import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functools import partial
import numpy as np


p_25 = partial(pd.Series.quantile, q=0.25)
p_25.__name__ = '25% Quantile'
p_75 = partial(pd.Series.quantile, q=0.75)
p_75.__name__ = '75% Quantile'


# Load the dataset
sales_data = pd.read_csv("sales.zip", compression='zip')
population_data = pd.read_csv("by_zip.csv", compression="infer")
print('loaded data')

# merge and drop
sales_data = sales_data.drop('County Number', axis=1)
sales_data = sales_data.drop('Iowa ZIP Code Tabulation Areas', axis=1)
sales_data = sales_data.drop('Iowa Watershed Sub-Basins (HUC 08)', axis=1)
sales_data = sales_data.drop('Iowa Watersheds (HUC 10)', axis=1)
sales_data = sales_data.drop('County Boundaries of Iowa', axis=1)
sales_data = sales_data.drop('Store Location', axis=1)
sales_data = sales_data.drop('US Counties', axis=1)
cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip")

#header
print("header")
print(cleaned_data.keys())

#LiterPerCounty
liter_per_county = cleaned_data.groupby('Zip Code')['Volume Sold (Liters)'].sum()

#Merge with another column from cleaned_data
liter_per_county = pd.merge(liter_per_county, cleaned_data[['Zip Code', 'population']].drop_duplicates(), on='Zip Code', how='left')

liter_per_county = liter_per_county.reset_index()
liter_per_county['Zip Code'] = liter_per_county['Zip Code'].astype(int)
liter_per_county['Zip Code'] = liter_per_county['Zip Code'].astype(str)
liter_per_county['Volume Sold (Liters)'] = liter_per_county['Volume Sold (Liters)'].astype(float)
liter_per_county['population'] = liter_per_county['population'].astype(float)
print(liter_per_county)

#Rechnung pro Kopf
liter_per_county['Liters per Capita'] = liter_per_county['Volume Sold (Liters)'] / liter_per_county['population']

#Sort by liters Top 10
sorted_for_liters = liter_per_county.sort_values(by='Volume Sold (Liters)', ascending=False)
top_10_county_liters = sorted_for_liters.head(10)

#Sort By Liters per Head Top 10
sorted_for_liters_per_capita = liter_per_county.sort_values(by='Liters per Capita', ascending=False)
top_10_zip_liters_per_head = sorted_for_liters_per_capita.head(10)

print("Top10 Liters/ZipCode:")
print(top_10_county_liters)
print("Top10 Liters/Head:")
print(top_10_zip_liters_per_head)

#Graph Top10 per head
fig = px.bar(top_10_zip_liters_per_head, x='Zip Code', y= 'Volume Sold (Liters)', title='Volume Sold per Zip Code Top 10')
fig.show()

#Graph Top10 perZipCode
fig = px.bar(top_10_county_liters, x='Zip Code', y= 'Liters per Capita', title='Volume Sold per Head per Zip Code Top 10')
fig.show()

# Calculate correlations
numeric_columns = top_10_zip_liters_per_head.select_dtypes(include=[np.number]).columns
correlation_matrix = top_10_zip_liters_per_head[numeric_columns].corr()

# Create a heatmap using Plotly Express
fig = px.imshow(correlation_matrix,
                labels=dict(color="Correlation"),
                x=correlation_matrix.index,
                y=correlation_matrix.columns,
                color_continuous_scale="Viridis")

fig.update_layout(title="Correlation Matrix",
                  xaxis_title="Variables",
                  yaxis_title="Variables")

# create png
fig.write_image("heatmapLiterPerZipHead.png")

# Show the plot
fig.show()