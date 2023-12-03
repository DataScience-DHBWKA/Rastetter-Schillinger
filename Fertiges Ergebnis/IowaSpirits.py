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

#Looking for nulls
for column in ['index', 'Date', 'City', 'Zip Code', 'County', 'Category',
       'category_name', 'Item Description', 'State Bottle Cost',
       'State Bottle Retail', 'Bottles Sold', 'sale_dollars',
       'Volume Sold (Liters)', 'Volume Sold (Gallons)', 'zip', 'population']:
    print(f'{column} nulls: {cleaned_data[column].isna().sum()}')





# Calculate correlations
numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
correlation_matrix = cleaned_data[numeric_columns].corr()

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
fig.write_image("heatmapAll.png")





# CategorySpirits

#TendencyToSpirits
print('TendencyToSpirits')
tendency_spirits = cleaned_data.groupby('category_name')['Volume Sold (Liters)'].sum().reset_index()
sorted_tendency_spirits = tendency_spirits.sort_values(by='Volume Sold (Liters)', ascending=False)

print(sorted_tendency_spirits)

fig = go.Figure(data=[go.Table(
    header=dict(values=['Category Name', 'Volume Sold (Liters)'],
                fill_color='crimson',
                align='left'),
    cells=dict(values=[sorted_tendency_spirits['category_name'], sorted_tendency_spirits['Volume Sold (Liters)']],
               fill_color='lavender',
               align='left'))
])
fig.show()
fig.write_image("TendencyToSpiritsTabelle.png")





# TendencyByZip

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
fig.write_image("TendencyToSpiritsTabelle2.png")
fig.show()





#Group and sort by Sales per Zip and Liters
grouped_data = cleaned_data.groupby(['Zip Code', 'category_name'])['Volume Sold (Liters)'].sum().reset_index()
sorted_data = grouped_data.sort_values(by=['Zip Code', 'Volume Sold (Liters)'], ascending=[True, False])
print(sorted_data)





# LiterPerCounty.py
print('LiterPerCounty')
#LiterPerCounty
liter_per_county = cleaned_data.groupby('Zip Code')['Volume Sold (Liters)'].sum()
#Merge with another column from cleaned_data
liter_per_county = pd.merge(liter_per_county, cleaned_data[['Zip Code', 'population']].drop_duplicates(), on='Zip Code', how='left')
#TypeCasting
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





#printLiterPer
print("Top10 Liters/ZipCode:")
print(top_10_county_liters)
print("Top10 Liters/Head:")
print(top_10_zip_liters_per_head)





#Graph Top10 per head
fig = px.bar(top_10_zip_liters_per_head, x='Zip Code', y= 'Volume Sold (Liters)', title='Volume Sold per Zip Code Top 10')
fig.show()
fig.write_image("BarGraphTop10ZipCodeLitersHead.png")
#Graph Top10 perZipCode
fig = px.bar(top_10_county_liters, x='Zip Code', y= 'Liters per Capita', title='Volume Sold per Head per Zip Code Top 10')
fig.show()
fig.write_image("BarGraphTop10ZipCodeLiters.png")





# Calculate correlations
numeric_columns = top_10_zip_liters_per_head.select_dtypes(include=[np.number]).columns
correlation_matrix = top_10_zip_liters_per_head[numeric_columns].corr()
# Graph heatmap LiterPerZipHead
fig = px.imshow(correlation_matrix,
                labels=dict(color="Correlation"),
                x=correlation_matrix.index,
                y=correlation_matrix.columns,
                color_continuous_scale="Viridis")
fig.update_layout(title="Correlation Matrix",
                  xaxis_title="Variables",
                  yaxis_title="Variables")
fig.write_image("heatmapLiterPerZipHead.png")
fig.show()





# Top10 für bessere Übersicht
zips = [50314,50320,51501,52240,52402,50266,50010,50613,52404,50317]
columns = ['Zip']
top10_zip_code_for_bottles_sold = pd.DataFrame(zips, columns=columns)
cleaned_data10 = cleaned_data.merge(top10_zip_code_for_bottles_sold, how="inner", left_on="Zip Code", right_on="Zip").reset_index()

#  Group and sort by Sales per Zip and Bottle
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





#VerkaufszahlenDatum

#Group and sort by Sales per Zip and Liters
sales_per_day_over_the_year = cleaned_data.groupby(['Date','Zip Code'])['Bottles Sold'].sum().reset_index()

sales_per_day_over_the_year['Date'] = pd.to_datetime(sales_per_day_over_the_year['Date'])
sales_per_day_over_the_year.set_index('Date', inplace=True)
sales_per_week_over_the_year = sales_per_day_over_the_year.resample('W-Mon').sum()
sales_per_week_over_the_year.reset_index(inplace=True)
sales_per_day_over_the_year.reset_index(inplace=True)

#Graph Bottles sold per week over the year
fig = px.line(sales_per_week_over_the_year, x='Date', y= 'Bottles Sold', title='Bottles sold over the year per week')
fig.show()
fig.write_image("SalesPerWeekOverTheYear.png")





# creating 'Week' as calendar week
cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'])
cleaned_data['Week'] = cleaned_data['Date'].dt.isocalendar().week


# Filter the data for the 7 days before christmas
christmas_data = cleaned_data[((cleaned_data['Date'] < '2022-12-24') & (cleaned_data['Date'] > '2022-12-17'))]

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





# Verkaufszahlen.py
print('Verkaufszahlen')
#dollar per county
dollar_per_county = cleaned_data.groupby('Zip Code')['sale_dollars'].sum()
dollar_per_county = dollar_per_county.reset_index()
dollar_per_county['Zip Code'] = dollar_per_county['Zip Code'].astype(int)
dollar_per_county['sale_dollars'] = dollar_per_county['sale_dollars'].astype(float)
print(dollar_per_county)
#Merge with another column from cleaned_data
dollar_per_county = pd.merge(dollar_per_county, cleaned_data[['Zip Code', 'population']].drop_duplicates(), on='Zip Code', how='left')
#Pro Kopf Rechnung
dollar_per_county['Dollar per head'] = dollar_per_county['sale_dollars'] / dollar_per_county['population']
# Sort by dollars Top 10
sorted_for_dollars = dollar_per_county.sort_values(by='sale_dollars', ascending=False)
sorted_for_dollars['Dollar per head'] = round(sorted_for_dollars['Dollar per head'], 2) 
top_10_zip = sorted_for_dollars.head(10)
# Sort by dollars per head Top 10
sorted_for_dollars_per_head = dollar_per_county.sort_values(by='Dollar per head', ascending=False)
sorted_for_dollars_per_head['Dollar per head'] = round(sorted_for_dollars_per_head['Dollar per head'], 2)
top_10_zip_head = sorted_for_dollars_per_head.head(10)
#Print
print("Top10 Dollar per Zip:")
print(top_10_zip)

#Creating tabels
fig = go.Figure(data=[go.Table(
    header=dict(values=['Zip Code', 'sale_dollars'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[top_10_zip['Zip Code'], top_10_zip['sale_dollars']],
               fill_color='lavender',
               align='left'))
])
fig.show()
fig.write_image("Top10 Dollar per Zip Tabelle.png")

print("Top10 Dollar per head:")
print(top_10_zip_head)
fig = go.Figure(data=[go.Table(
    header=dict(values=['Zip Code', 'sale_dollars'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[top_10_zip_head['Zip Code'], top_10_zip_head['sale_dollars']],
               fill_color='lavender',
               align='left'))
])
fig.show()
fig.write_image("Top10 Dollar per head Tabelle.png")