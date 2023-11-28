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
zips = [50314,50320,51501,52240,52402,50266,50010,50613,52404,50317]
columns = ['Zip']
top10_zip_code_for_bottles_sold = pd.DataFrame(zips, columns=columns)
print(top10_zip_code_for_bottles_sold)
cleaned_data10 = cleaned_data.merge(top10_zip_code_for_bottles_sold, how="inner", left_on="Zip Code", right_on="Zip").reset_index()

#  Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year10 = cleaned_data10.groupby(['Date', 'Zip Code'])['Bottles Sold'].sum().reset_index()

sales_per_day_over_the_year10['Date'] = pd.to_datetime(sales_per_day_over_the_year10['Date'])
sales_per_day_over_the_year10.set_index('Date', inplace=True)

# Resample to get weekly sales per zip code
sales_per_week_over_the_year10 = sales_per_day_over_the_year10.groupby(['Zip Code', pd.Grouper(freq='W-Mon')])['Bottles Sold'].sum().reset_index()

# Create a line plot
fig = px.line(sales_per_week_over_the_year10, x='Date', y='Bottles Sold', color='Zip Code',
              title='Bottles Sold Over Time by Zip Code',
              labels={'Date': 'Date', 'Bottles Sold': 'Bottles Sold', 'Zip Code': 'Zip Code'})

fig.show()

#create png
fig.write_image("VerkaufzahlenDateZipGraphTop10.png")