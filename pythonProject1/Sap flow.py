import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
Sap_flow_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/Sap flow data.xlsx')
df = pd.DataFrame(Sap_flow_data)

# Display original data structure
#print("Original Data:")
#print(df.head(2))

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Normalize numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
scaler = MinMaxScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Convert 'Date & time' column to datetime format, then split into 'Date' and 'Time'
df['Date&time'] = pd.to_datetime(df['Date&time'])
df['Date'] = df['Date&time'].dt.date
df['Time'] = df['Date&time'].dt.time
df = df.drop(columns=['Date&time'])

# Calculate the average of every 4 hours, ignoring NaN values
# Create averaged columns for each 4-hour period
averaged_columns = {}
for col in numeric_columns:
    # Calculate rolling mean while dropping NaN values within each window
    averaged_columns[col] = df[col].rolling(window=4, min_periods=1).apply(lambda x: x.dropna().mean())

# Create a new DataFrame with measurements starting from the first row and then every 4 hours
averaged_df = pd.DataFrame({col: averaged_columns[col].iloc[::4].reset_index(drop=True) for col in numeric_columns})
averaged_df['Date'] = df['Date'].iloc[::4].reset_index(drop=True)
averaged_df['Time'] = df['Time'].iloc[::4].reset_index(drop=True)

# Normalize the averaged values between 0 and 1
scaler = MinMaxScaler()
columns_to_normalize = list(averaged_columns.keys())  # Convert dict_keys to a list
averaged_df[columns_to_normalize] = scaler.fit_transform(averaged_df[columns_to_normalize])

# Round values to four decimal places
averaged_df[columns_to_normalize] = averaged_df[columns_to_normalize].round(4)


# Calculate the new columns based on the given patterns
df['D type irrigation avg'] = df.filter(regex=r"_D_").mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").mean(axis=1)
df['100% water'] = df.filter(regex=r"_100$").mean(axis=1)
df['50% water'] = df.filter(regex=r"_50$").mean(axis=1)

# Display the updated DataFrame
print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water', 'Date', 'Time']].head())

# Display the final result
print(averaged_df.head())


import matplotlib.pyplot as plt

# Plotting
plt.figure(figsize=(14, 8))

# Plot sap flow based on irrigation type
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['D type irrigation avg'], label='D Type Irrigation Avg')
plt.plot(df['Date'], df['E type irrigation avg'], label='E Type Irrigation Avg')
plt.xlabel('Date')
plt.ylabel('Sap Flow (Irrigation Type)')
plt.title('Sap Flow Based on Irrigation Type')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

# Plot sap flow based on water amount
plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['100% water'], label='100% Water')
plt.plot(df['Date'], df['50% water'], label='50% Water')
plt.xlabel('Date')
plt.ylabel('Sap Flow (Water Amount)')
plt.title('Sap Flow Based on Water Amount')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
