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
cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip").reset_index()

#header
print("header")
print(cleaned_data.keys())

#Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year = cleaned_data.groupby(['Date','Zip Code'])['Bottles Sold'].sum().reset_index()
# sorted_data = grouped_data.sort_values(by=['Zip Code', 'Volume Sold (Liters)'], ascending=[True, False])

sales_per_day_over_the_year['Date'] = pd.to_datetime(sales_per_day_over_the_year['Date'])
sales_per_day_over_the_year.set_index('Date', inplace=True)
sales_per_week_over_the_year = sales_per_day_over_the_year.resample('W-Mon').sum()
sales_per_week_over_the_year.reset_index(inplace=True)
sales_per_day_over_the_year.reset_index(inplace=True)

print(sales_per_day_over_the_year)
print(sales_per_week_over_the_year)

# #Graph Bottles sold per week over the year
# fig = px.line(sales_per_week_over_the_year, x='Date', y= 'Bottles Sold', title='Bottles sold over the year per week')
# fig.show()

# #Graph Bottles sold per week over the year
# fig = px.line(sales_per_week_over_the_year, x='Date', y= 'Bottles Sold', title='Bottles sold over the year')
# fig.show()

fig = px.line(sales_per_week_over_the_year, x='Date', y='Bottles Sold', color='Zip Code',
              title='Alcohol Consumption Over Time by Zip Code',
              labels={'Date': 'Date', 'Bottles Sold': 'Bottles Sold', 'Zip Code': 'Zip Code'})

fig.show()