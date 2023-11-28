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

#Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year = cleaned_data.groupby(['Date','Zip Code'])['Bottles Sold'].sum().reset_index()

sales_per_day_over_the_year['Date'] = pd.to_datetime(sales_per_day_over_the_year['Date'])
sales_per_day_over_the_year.set_index('Date', inplace=True)
sales_per_week_over_the_year = sales_per_day_over_the_year.resample('W-Mon').sum()
sales_per_week_over_the_year.reset_index(inplace=True)
sales_per_day_over_the_year.reset_index(inplace=True)

print(sales_per_day_over_the_year)
print(sales_per_week_over_the_year)

#Graph Bottles sold per week over the year
fig = px.line(sales_per_week_over_the_year, x='Date', y= 'Bottles Sold', title='Bottles sold over the year per week')
fig.show()
fig.write_image("SalesPerWeekOverTheYear.png")


#Graph Balken
fig = px.bar(sales_per_week_over_the_year, x='Date', y= 'Bottles Sold', title='Bottles sold over the year')
fig.show()