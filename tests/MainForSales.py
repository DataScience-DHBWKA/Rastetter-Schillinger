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

print('header')
print(cleaned_data.keys())

#Looking for nulls
print('nulls')
for column in ['index', 'Date', 'City', 'Zip Code', 'County', 'Category',
       'category_name', 'Item Description', 'State Bottle Cost',
       'State Bottle Retail', 'Bottles Sold', 'sale_dollars',
       'Volume Sold (Liters)', 'Volume Sold (Gallons)', 'zip', 'population']:
    print(f'{column} nulls: {cleaned_data[column].isna().sum()}')

# CategorySpirits

#TendencyToSpirits
print('TendencyToSpirits')
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
fig.write_image("TendencyToSpiritsTabelle.png")


# TendencyByZip

#Group and sort by Sales per Zip and Liters
grouped_data = cleaned_data.groupby(['Zip Code', 'category_name'])['Volume Sold (Liters)'].sum().reset_index()
sorted_data = grouped_data.sort_values(by=['Zip Code', 'Volume Sold (Liters)'], ascending=[True, False])
print(sorted_data)

#Verkäufe gewisser Spirituosen vor bestimmten Feiertagen


#VerkaufszahlenDatum

#Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year = cleaned_data.groupby(['Date','Zip Code',])['Bottles Sold'].sum().reset_index()

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