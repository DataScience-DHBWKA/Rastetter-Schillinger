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
grouped_data = cleaned_data.groupby(['Zip Code', 'category_name'])['Volume Sold (Liters)'].sum().reset_index()
sorted_data = grouped_data.sort_values(by=['Zip Code', 'Volume Sold (Liters)'], ascending=[True, False])

print(sorted_data)