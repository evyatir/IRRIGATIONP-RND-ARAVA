import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Set the display option to show all columns
pd.set_option('display.max_columns', None)


# Load the Excel file
tdr_water_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/tdr water.xlsx')
df = pd.DataFrame(tdr_water_data)

# Display original data structure
print("Original Data:")
print(df.head(2))

# Assuming your DataFrame is named 'df' and the 'dt' column is of datetime type
# First, ensure 'dt' is in datetime format
df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

# Create separate date and time columns
df['Date'] = df['dt'].dt.date
df['Time'] = df['dt'].dt.time

# keep every for hours measure
df = df[df['Time'].astype(str).str.endswith("00:00") & (df['dt'].dt.hour % 4 == 0)]


# Round all numeric columns to 4 decimal places
df = df.round(4)

# Optionally, drop the original 'dt' column
df = df.drop(columns=['dt'])

# Reset index to start from 1
df = df.reset_index(drop=True)
df.index += 1


df['D type irrigation avg'] = df.filter(regex=r"_D_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['100% water'] = df.filter(regex=r"_100_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['50% water'] = df.filter(regex=r"_50_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['40 cm depth'] = df.filter(regex=r"_40").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['80 cm depth'] = df.filter(regex=r"_80").apply(pd.to_numeric, errors='coerce').mean(axis=1)



print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water','40 cm depth','80 cm depth',  'Date', 'Time']].head())



import matplotlib.pyplot as plt
"first graph"
# Prepare data for plotting
depths = ['40 cm depth', '80 cm depth']
d_type_values = [df['D type irrigation avg'].mean(), df['80 cm depth'].mean()]
e_type_values = [df['E type irrigation avg'].mean(), df['80 cm depth'].mean()]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(depths, d_type_values, marker='o', label='D Type Irrigation')
plt.plot(depths, e_type_values, marker='o', label='E Type Irrigation')

# Customizing the plot
plt.title('Effect of Irrigation Type on Sensor Depths (40 cm vs 80 cm)')
plt.xlabel('Sensor Depth')
plt.ylabel('Average Sensor Value')
plt.legend()
plt.grid()

# Display the plot
plt.show()


"second graph"

import matplotlib.pyplot as plt

# Calculate the average values for 50% water for each irrigation type
d_type_50_percent = df.filter(regex=r"T\d+_D_50").apply(pd.to_numeric, errors='coerce').mean(axis=1).mean()
e_type_50_percent = df.filter(regex=r"T\d+_E_50").apply(pd.to_numeric, errors='coerce').mean(axis=1).mean()

# Data for plotting
irrigation_types = ['D Type', 'E Type']
average_values = [d_type_50_percent, e_type_50_percent]

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(irrigation_types, average_values, color=['blue', 'green'])

# Customizing the plot
plt.title('Comparison of D and E Irrigation Types at 50% Water')
plt.xlabel('Irrigation Type')
plt.ylabel('Average Sensor Value')
plt.ylim(0, max(average_values) * 1.1)  # Adjust y-axis for better visibility
plt.grid(axis='y')

# Display the plot
plt.show()



