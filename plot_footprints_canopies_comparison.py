import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_buildings = {
    'PWS': ['PWS20', 'PWS40', 'PWS60', 'PWS80', 'PWS100', 'PWS150', 'PWS200'],
    'Total Footprint Area (sq. m)': [132718.424, 464189.275, 1008682.0307, 1757363.5528, 2647837.5403, 5633673.8242, 9522654.4299],
    'Mean Building Height (m)': [9.127, 9.084, 9.009, 9.025, 9.008, 9.018, 9.007],
    'Coverage (%)': [13.49, 11.91, 11.62, 11.49, 11.18, 10.76, 10.40]
}
# Create buildings dataframe
df_buildings = pd.DataFrame(data_buildings)
# Convert PWS to a numeric value for easier plotting
df_buildings['PWS_Value'] = df_buildings['PWS'].str.extract(r'(\d+)').astype(int)

# Create trees dataframe
data_canopy = {
    "PWS": ["PWS20", "PWS40", "PWS60", "PWS80", "PWS100", "PWS150", "PWS200"],
    "Total Canopy Area (sq. m)": [294183.0, 1192810.0, 3057278.0, 5460120.0, 8534680.0, 18985030.0, 33199458.0],
    "Mean Canopy Height (m)": [2.860, 2.910, 3.000, 3.051, 3.092, 3.147, 3.172],
    "Coverage (%)": [29.79, 30.48, 35.07, 35.56, 35.88, 36.13, 36.11]
}

df_canopy = pd.DataFrame(data_canopy)
# Convert PWS to a numeric value for easier plotting
df_canopy['PWS_Value'] = df_canopy['PWS'].str.extract(r'(\d+)').astype(int)

# Assuming df_buildings and df_canopy are already defined and loaded
# Plotting comparative growth trends
fig, axes = plt.subplots(1, 1, figsize=(12, 6))
sns.lineplot(x='PWS_Value', y='Total Footprint Area (sq. m)', data=df_buildings, marker='o', label='Building Footprint', ax=axes)
sns.lineplot(x='PWS_Value', y='Total Canopy Area (sq. m)', data=df_canopy, marker='o', label='Canopy Area', ax=axes)
axes.set_title('Growth Trends of Building Footprints and Canopy Areas')
axes.set_xlabel('Personal Weather Systems (PWS)')
axes.set_ylabel('Area (sq. m) * 10^6')
axes.legend()
plt.show()

