import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
frond_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/Frond data 1.xlsx')
df = pd.DataFrame(frond_data)

# Display original data structure
print("Original Data:")
print(df.head(2))

# Normalize numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
scaler = MinMaxScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Ensure 'Date & time' is in datetime format, then split into 'Date' and 'Time'
df['Date & time'] = pd.to_datetime(df['Date & time'])
df['Date'] = df['Date & time'].dt.date
df['Time'] = df['Date & time'].dt.time
df = df.drop(columns=['Date & time'])

#keep only every four hours measure
df = df[(df['Time'].astype(str).str.endswith("00:00")) & (df['Time'].apply(lambda t: t.hour % 4 == 0))]


# Round all numeric columns to 4 decimal places
df = df.round(4)

# Reset index to start from 1
df = df.reset_index(drop=True)
df.index += 1

# Calculate the new columns based on the given patterns
df['D type irrigation avg'] = df.filter(regex=r"_D_").mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").mean(axis=1)
df['100% water'] = df.filter(regex=r"_100$").mean(axis=1)
df['50% water'] = df.filter(regex=r"_50$").mean(axis=1)

# Calculate growth rate (f') for each type
df['Growth rate 100% water'] = df['100% water'].diff().fillna(0)
df['Growth rate 50% water'] = df['50% water'].diff().fillna(0)
df['Growth rate D type irrigation'] = df['D type irrigation avg'].diff().fillna(0)
df['Growth rate E type irrigation'] = df['E type irrigation avg'].diff().fillna(0)

# Apply rolling average with a window of 4 for smoother lines
df['Smooth Growth rate 100% water'] = df['Growth rate 100% water'].rolling(window=4, min_periods=1).mean()
df['Smooth Growth rate 50% water'] = df['Growth rate 50% water'].rolling(window=4, min_periods=1).mean()
df['Smooth Growth rate D type irrigation'] = df['Growth rate D type irrigation'].rolling(window=4, min_periods=1).mean()
df['Smooth Growth rate E type irrigation'] = df['Growth rate E type irrigation'].rolling(window=4, min_periods=1).mean()


# Display the updated DataFrame
print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water', 'Date', 'Time']].head())



# FIRST GRAPH - COMPARE BETWEEN the amount of irrigation
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['100% water'], label='100% water')
plt.plot(df['Date'], df['50% water'], label='50% water')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('The effect of the amount of water on the growth of the frond')


# Set x-axis major ticks to be more frequent (twice as crowded)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Set smaller interval
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=90))  # Add minor ticks every 12 hours if desired
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for readability and improve layout
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# SECOND GRAPH - COMPARE BETWEEN Irrigation methods
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['D type irrigation avg'], label='D type irrigation avg')
plt.plot(df['Date'], df['E type irrigation avg'], label='E type irrigation avg')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('The effect of the irrigation method on the growth of the frond')


# Set x-axis major ticks to be more frequent (twice as crowded)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Set smaller interval
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=90))  # Add minor ticks every 12 hours if desired
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for readability and improve layout
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Ensure 'Date' is in datetime format for easier filtering by month and year
df['Date'] = pd.to_datetime(df['Date'])

# Get the unique year-month combinations in the data
year_months = df['Date'].dt.to_period('M').unique()

# Loop through each month and plot the growth rates for that month
for period in year_months:
    # Filter the DataFrame for the current month
    monthly_data = df[df['Date'].dt.to_period('M') == period]

    # Plotting smoothed growth rate for 100% and 50% water levels for the month
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['Date'], monthly_data['Smooth Growth rate 100% water'], label='Smoothed Growth rate 100% water', linewidth=2)
    plt.plot(monthly_data['Date'], monthly_data['Smooth Growth rate 50% water'], label='Smoothed Growth rate 50% water', linewidth=2, linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Growth rate (f\')')
    plt.title(f'Smoothed Growth Rate of the Frond with Different Water Levels for {period}')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.ylim(0, 0.035)  # Set y-axis range
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plotting smoothed growth rate for D and E irrigation types for the month
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['Date'], monthly_data['Smooth Growth rate D type irrigation'], label='Smoothed Growth rate D type irrigation', linewidth=2)
    plt.plot(monthly_data['Date'], monthly_data['Smooth Growth rate E type irrigation'], label='Smoothed Growth rate E type irrigation', linewidth=2, linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Growth rate (f\')')
    plt.title(f'Smoothed Growth Rate of the Frond with Different Irrigation Methods for {period}')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.ylim(0, 0.035)  # Set y-axis range
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()





