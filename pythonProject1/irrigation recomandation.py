import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
Sap_flow_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/irregration reccomandations.xlsx')
df = pd.DataFrame(Sap_flow_data)

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Display original data structure
print("Original Data:")
print(df.head(2))

import matplotlib.pyplot as plt

# Assuming the DataFrame is called df and has the columns: 'month', 'ETo pen (mm)', 'Kc-fruit', and 'Recommendation'

# Plotting
plt.figure(figsize=(12, 6))

# Plot ETo per month
plt.plot(df['month'], df['ETo pen (mm)'], label='ETo per month', marker='o')

# Plot Kc-fruit per month
plt.plot(df['month'], df['Kc-fruit'], label='Kc-fruit per month', marker='o')

# Plot Recommendation per month
plt.plot(df['month'], df['Recommendation'], label='Recommendation per month', marker='o')

# Calculate half of the Recommendation
df['Half Recommendation'] = df['Recommendation'] / 2

# Plot Half of Recommendation per month
plt.plot(df['month'], df['Half Recommendation'], label='Half of Recommendation per month', linestyle='--', marker='o')


# Customize the plot
plt.xlabel('Month')
plt.ylabel('Values')
plt.title('Monthly ETo, Kc-fruit, and Recommendation')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()
