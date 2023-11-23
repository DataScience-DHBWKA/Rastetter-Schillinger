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
sales_data = sales_data.drop(['County Number', 'Iowa ZIP Code Tabulation Areas',
                              'Iowa Watershed Sub-Basins (HUC 08)', 'Iowa Watersheds (HUC 10)',
                              'County Boundaries of Iowa', 'Store Location', 'US Counties'], axis=1)

cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip").reset_index()



# Top10 für bessere Übersicht
# top10_zip_code_for_bottles_sold = ['50314.0','50320.0','51501.0','52240.0','52402.0','50266.0','50010.0','50613.0','52404.0','50317.0']
# cleaned_data.loc[~cleaned_data['Zip Code'].isin(top10_zip_code_for_bottles_sold), 'Zip Code'] = None



# Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year = cleaned_data.groupby(['Date', 'Zip Code'])['Bottles Sold'].sum().reset_index()

sales_per_day_over_the_year['Date'] = pd.to_datetime(sales_per_day_over_the_year['Date'])
sales_per_day_over_the_year.set_index('Date', inplace=True)

# Resample to get weekly sales per zip code
sales_per_week_over_the_year = sales_per_day_over_the_year.groupby(['Zip Code', pd.Grouper(freq='W-Mon')])['Bottles Sold'].sum().reset_index()

# Create a line plot
fig = px.line(sales_per_week_over_the_year, x='Date', y='Bottles Sold', color='Zip Code',
              title='Bottles Sold Over Time by Zip Code',
              labels={'Date': 'Date', 'Bottles Sold': 'Bottles Sold', 'Zip Code': 'Zip Code'})

fig.show()

# # create png
# # fig.write_image("VerkaufzahlenDateZipGraph.png")