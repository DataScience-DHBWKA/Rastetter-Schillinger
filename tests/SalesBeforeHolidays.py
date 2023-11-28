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

# creating 'Week' as calendar week
cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'])
cleaned_data['Week'] = cleaned_data['Date'].dt.isocalendar().week


# Filter the data for the the 7 days before christmas
christmas_data = cleaned_data[((cleaned_data['Date'] < '2022-12-24') & (cleaneed_data['Date'] > '2022-12-17'))]

# Group by category and sum the bottles sold
category_sales = christmas_data.groupby('category_name')['Bottles Sold'].sum().reset_index()

# Sort the data and get the top 10
top_10_categories = category_sales.nlargest(10, 'Bottles Sold')

# Create a table using plotly.graph_objects
fig = go.Figure(data=[go.Table(
    header=dict(values=['Category', 'Bottles Sold']),
    cells=dict(values=[top_10_categories['category_name'], top_10_categories['Bottles Sold']])
)])

# save the table
fig.write_image("SalesBeforeChristmasTop10.png")


# Filter the data for the the 7 days before halloween
halloween_data = cleaned_data[((cleaned_data['Date'] < '2022-10-31') & (cleaned_data['Date'] > '2022-10-24'))]

# Group by category and sum the bottles sold
category_sales = halloween_data.groupby('category_name')['Bottles Sold'].sum().reset_index()

# Sort the data and get the top 10
top_10_categories = category_sales.nlargest(10, 'Bottles Sold')

# Create a table using plotly.graph_objects
fig = go.Figure(data=[go.Table(
    header=dict(values=['Category', 'Bottles Sold']),
    cells=dict(values=[top_10_categories['category_name'], top_10_categories['Bottles Sold']])
)])

# save the table
fig.write_image("SalesBeforeHalloweenTop10.png")
