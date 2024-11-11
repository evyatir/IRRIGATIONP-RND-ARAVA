import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set the display option to show all columns
#pd.set_option('display.max_columns', None)

# Load the Excel file
tdr_salt_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/tensiometer data.xlsx')
df = pd.DataFrame(tdr_salt_data)

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

#print(df.head())

df['D type irrigation avg'] = df.filter(regex=r"_D_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['100% water'] = df.filter(regex=r"_100_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['50% water'] = df.filter(regex=r"_50_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['40 cm depth'] = df.filter(regex=r"_40").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['80 cm depth'] = df.filter(regex=r"_80").apply(pd.to_numeric, errors='coerce').mean(axis=1)


print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water','40 cm depth','80 cm depth',  'Date', 'Time']].head())

plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['100% water'], label='100% water')
plt.plot(df['Date'], df['50% water'], label='50% water')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('The effect of the amount of water on the growth of tensiometer')


# Set x-axis major ticks to be more frequent (twice as crowded)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Set smaller interval
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=90))  # Add minor ticks every 12 hours if desired
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for readability and improve layout
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()