from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
Sap_flow_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/Stem dendrometer.xlsx')
df = pd.DataFrame(Sap_flow_data)

# Fill NaN values using interpolation
df = df.interpolate(method='linear', limit_direction='both')

# Separate the numeric columns from the date column
date_column = df['Date']
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Apply the scaler only to numeric columns
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Add back the date column
df['Date'] = date_column


df[numeric_columns] = df[numeric_columns].round(4)

# Display the normalized data
print("Data after normalization between 0 and 1 (excluding Date):")
print(df.head(2))

# Calculate the new columns based on the given patterns
df['D type irrigation avg'] = df.filter(regex=r"_D_").mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").mean(axis=1)
df['100% water'] = df.filter(regex=r"_100$").mean(axis=1)
df['50% water'] = df.filter(regex=r"_50$").mean(axis=1)

# Display the updated DataFrame
print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water', 'Date']].head())

# Set the 'Date' column as the index for plotting
df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' is in datetime format
df.set_index('Date', inplace=True)

# Plot dendrometer values for different categories over time
plt.figure(figsize=(12, 8))

# Plot 'D type irrigation avg' and 'E type irrigation avg'
plt.plot(df.index, df['D type irrigation avg'], label='D type irrigation avg', linestyle='-', marker='o')
plt.plot(df.index, df['E type irrigation avg'], label='E type irrigation avg', linestyle='-', marker='o')

# Plot '100% water' and '50% water'
plt.plot(df.index, df['100% water'], label='100% water', linestyle='--', marker='x')
plt.plot(df.index, df['50% water'], label='50% water', linestyle='--', marker='x')

# Customize the plot
plt.title("Dendrometer Values According to Water Levels and Irrigation Type")
plt.xlabel("Date")
plt.ylabel("Normalized Dendrometer Value")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()