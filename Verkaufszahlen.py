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

# merge
sales_data = sales_data.drop('County Number', axis=1)
sales_data = sales_data.drop('Iowa ZIP Code Tabulation Areas', axis=1)
sales_data = sales_data.drop('Iowa Watershed Sub-Basins (HUC 08)', axis=1)
sales_data = sales_data.drop('Iowa Watersheds (HUC 10)', axis=1)
sales_data = sales_data.drop('County Boundaries of Iowa', axis=1)
sales_data = sales_data.drop('Store Location', axis=1)
sales_data = sales_data.drop('US Counties', axis=1)
cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip")

#header
print("header")
print(cleaned_data.keys())

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
print("Top10 Dollar per head:")
print(top_10_zip_head)