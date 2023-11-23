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


print("header")
print(population_data.keys())
print(sales_data.keys())

# merge
cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip")


# Clean the dataset
sales_data["sale_dollars"] = sales_data["sale_dollars"].astype(float)

# gruppieren nach PLZ und Summe über die Verkaufssumme und Anzahl Verkäufe pro PLZ
sales_by_zip_grouped = sales_data.groupby('Zip Code').agg(sale_dollars=('sale_dollars', np.sum), num_sales=('sale_dollars', np.size)).reset_index()

sales_data = sales_data.drop('County Number', axis=1)
sales_data = sales_data.drop('Iowa ZIP Code Tabulation Areas', axis=1)
sales_data = sales_data.drop('Iowa Watershed Sub-Basins (HUC 08)', axis=1)
sales_data = sales_data.drop('Iowa Watersheds (HUC 10)', axis=1)
sales_data = sales_data.drop('County Boundaries of Iowa', axis=1)
sales_data = sales_data.drop('Store Location', axis=1)
sales_data = sales_data.drop('US Counties', axis=1)

for column in ['Invoice/Item Number', 'Date', 'store_number', 'Store Name', 'Address',
       'City', 'Zip Code', 'County',
       'Category', 'category_name', 'Vendor Number', 'Vendor Name',
       'Item Number', 'Item Description', 'Pack', 'Bottle Volume (ml)',
       'State Bottle Cost', 'State Bottle Retail', 'Bottles Sold',
       'sale_dollars', 'Volume Sold (Liters)', 'Volume Sold (Gallons)', 'zip', 'population']:
    print(f'{column} nulls: {cleaned_data[column].isna().sum()}')