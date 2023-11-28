import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functools import partial
import numpy as np

# Load the dataset
sales_data = pd.read_csv("sales.zip", compression='zip')
population_data = pd.read_csv("by_zip.csv", compression="infer")
print('loaded data')

# merge and drop
sales_data = sales_data.drop(['Invoice/Item Number','County Number', 'Iowa ZIP Code Tabulation Areas',
                              'store_number', 'Store Name','Address','Vendor Number', 'Vendor Name', 'Item Number',
                              'Iowa Watershed Sub-Basins (HUC 08)', 'Iowa Watersheds (HUC 10)','Pack', 'Bottle Volume (ml)',
                              'County Boundaries of Iowa', 'Store Location', 'US Counties'], axis=1)

cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip").reset_index()


#header
print("header")
print(cleaned_data.keys())

#TendencyToSpirits
tendency_spirits = cleaned_data.groupby('category_name')['Volume Sold (Liters)'].sum().reset_index()
sorted_tendency_spirits = tendency_spirits.sort_values(by='Volume Sold (Liters)', ascending=False)

print(sorted_tendency_spirits)

fig = go.Figure(data=[go.Table(
    header=dict(values=['Category Name', 'Volume Sold (Liters)'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[sorted_tendency_spirits['category_name'], sorted_tendency_spirits['Volume Sold (Liters)']],
               fill_color='lavender',
               align='left'))
])

fig.show()