from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
Sap_flow_data = pd.read_excel('/Users/evyataryatir/Desktop/STARSHIP ARAVA RND/DATA tables/eto & vpd.xlsx')
df = pd.DataFrame(Sap_flow_data)

#print(df.head(2))

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

print(df.head())


# Convert 'Date' and 'Time' columns back into a single datetime index for plotting
df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

# Plot 1: eto and vpd over time
plt.figure(figsize=(12, 6))
plt.plot(df['Datetime'], df['eto'], label='eto', marker='o', linestyle='-')
plt.plot(df['Datetime'], df['vpd'], label='vpd', marker='x', linestyle='--')
plt.title("ETO and VPD Over Time")
plt.xlabel("Time")
plt.ylabel("Values")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate the ratio between eto and vpd
df['eto_vpd_ratio'] = df['eto'] / df['vpd']

# Plot 2: Ratio of eto to vpd over time
plt.figure(figsize=(12, 6))
plt.plot(df['Datetime'], df['eto_vpd_ratio'], label='ETO/VPD Ratio', marker='s', color='purple')
plt.title("Ratio of ETO to VPD Over Time")
plt.xlabel("Time")
plt.ylabel("ETO/VPD Ratio")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
