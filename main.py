import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functools import partial
import numpy as np
import seaborn as sns


p_25 = partial(pd.Series.quantile, q=0.25)
p_25.__name__ = '25% Quantile'
p_75 = partial(pd.Series.quantile, q=0.75)
p_75.__name__ = '75% Quantile'


# Load the dataset
sales_data = pd.read_csv("sales.zip", compression='zip')
population_data = pd.read_csv("by_zip.csv", compression="infer")
print('loaded data')


print("header")
print(population_data.keys())

print(sales_data.keys())
#print(population_data["ZCTA"].apply(lambda x: re.sub('.+(\d+)', '$1', x)))


#print("merged")
#print(sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip").head)

# Clean the dataset
#sales_data = sales_data.dropna(subset=["category_name", "sale_dollars"])
sales_data["sale_dollars"] = sales_data["sale_dollars"].astype(float)
#sales_data = sales_data.dropna()


category_sales = sales_data.groupby('category_name')['sale_dollars'].sum().reset_index()
category_sales_sorted = category_sales.sort_values("sale_dollars")

print('summed')

# gruppieren nach PLZ und Summe über die Verkaufssumme und Anzahl Verkäufe pro PLZ
sales_by_zip_grouped = sales_data.groupby('Zip Code').agg(sale_dollars=('sale_dollars', np.sum), num_sales=('sale_dollars', np.size)).reset_index()
# join der populatio data pro PLZ

sales_data = sales_data.drop('County Number', axis=1)

for column in ['Invoice/Item Number', 'Date', 'store_number', 'Store Name', 'Address',
       'City', 'Zip Code', 'Store Location', 'County',
       'Category', 'category_name', 'Vendor Number', 'Vendor Name',
       'Item Number', 'Item Description', 'Pack', 'Bottle Volume (ml)',
       'State Bottle Cost', 'State Bottle Retail', 'Bottles Sold',
       'sale_dollars', 'Volume Sold (Liters)', 'Volume Sold (Gallons)',
       'Iowa ZIP Code Tabulation Areas', 'Iowa Watershed Sub-Basins (HUC 08)',
       'Iowa Watersheds (HUC 10)', 'County Boundaries of Iowa', 'US Counties']:
    print(f'{column} nulls: {sales_data[column].isna().sum()}')

sales_by_zip = sales_by_zip_grouped.merge(population_data, how="inner", left_on="Zip Code", right_on="zip")
sales_by_zip['sales_per_capita'] = sales_by_zip['sale_dollars']/sales_by_zip['population']
sales_by_zip["zip"] = sales_by_zip["zip"].astype("string")
sales_by_zip = sales_by_zip.sort_values("sales_per_capita")

consumption_by_zip = sales_data.groupby('Zip Code').agg(consumption=('Volume Sold (Liters)', np.sum), num_sales=('Volume Sold (Liters)', np.size)).reset_index().merge(population_data, how="inner", left_on="Zip Code", right_on="zip")
consumption_by_zip['consumption_per_capita'] = consumption_by_zip['consumption']/consumption_by_zip['population']
consumption_by_zip = consumption_by_zip.sort_values("consumption_per_capita")
consumption_by_zip["zip"] = consumption_by_zip["zip"].astype("string")


print(sales_by_zip['sales_per_capita'].agg(['mean','median', 'max', 'min', p_25, p_75]))
print(sales_by_zip.tail(10))


# Create a box plot
fig = px.bar(category_sales_sorted, x="category_name", y="sale_dollars", labels={"category_name": "Product Category", "sale_dollars": "total sales"})
#fig.show()
fig.write_image('Sale by category.png')

fig = px.bar(sales_by_zip.sort_values("zip"), x="zip", y="sale_dollars", labels={"zip": "ZIP", "sale_dollars": "total sales"})
#fig.show()
fig.write_image('Sale by ZIP.png')

fig = px.bar(sales_by_zip.sort_values("zip"), x="zip", y="sales_per_capita", labels={"zip": "ZIP", "sales_per_capita": "Sales per capita"})
#fig.show()
fig.write_image('Sale per capita by ZIP.png')

fig = px.bar(consumption_by_zip.sort_values("zip"), x="zip", y="consumption_per_capita", labels={"zip": "ZIP", "consumption_per_capita": "Consumption per capita"})
fig.write_image('Consumption per capita by ZIP.png')

fig = px.box(sales_by_zip['sales_per_capita'])
fig.write_image('Sale per capita box.png')

fig = px.box(consumption_by_zip['consumption_per_capita'])
fig.write_image('Consumption per capita box.png')

sbct10 = sales_by_zip.tail(10)

fig = go.Figure(data=[go.Table(header=dict(values=['zip', 'population', 'num_sales', 'sales_per_capita' ]), cells=dict(values=[sbct10['zip'],
                                                                                                                         sbct10['population'],
                                                                                                                         sbct10['num_sales'], 
                                                                                                                        sbct10['sales_per_capita']]))])
fig.write_image('Sale per capita top 10.png')