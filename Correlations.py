import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functools import partial
import numpy as np

# Load the dataset
sales_data = pd.read_csv("sales.zip", compression='zip')
population_data = pd.read_csv("by_zip.csv", compression="infer")
print('loaded data')

# Merge and drop unnecessary columns
sales_data = sales_data.drop(['County Number', 'Iowa ZIP Code Tabulation Areas',
                              'Iowa Watershed Sub-Basins (HUC 08)', 'Iowa Watersheds (HUC 10)',
                              'County Boundaries of Iowa', 'Store Location', 'US Counties'], axis=1)

cleaned_data = sales_data.merge(population_data, how="inner", left_on="Zip Code", right_on="zip").reset_index()

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

# Show the plot
# fig.show()