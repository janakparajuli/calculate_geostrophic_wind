import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    "PWS": ["PWS20", "PWS40", "PWS60", "PWS80", "PWS100", "PWS150", "PWS200"],
    "Total Canopy Area (sq. m)": [294183.0, 1192810.0, 3057278.0, 5460120.0, 8534680.0, 18985030.0, 33199458.0],
    "Mean Canopy Height (m)": [2.860, 2.910, 3.000, 3.051, 3.092, 3.147, 3.172],
    "Coverage (%)": [29.79, 30.48, 35.07, 35.56, 35.88, 36.13, 36.11]
}

df_canopy = pd.DataFrame(data)
# Convert PWS to a numeric value for easier plotting
df_canopy['PWS_Value'] = df_canopy['PWS'].str.extract(r'(\d+)').astype(int)

# Plotting Total Canopy Area vs. PWS
fig, axes = plt.subplots(1, 3, figsize=(12, 6))
sns.lineplot(x='PWS_Value', y='Total Canopy Area (sq. m)', marker='o', data=df_canopy, ax = axes[0])
axes[0].set_title('Total Canopy Area vs. PWS')
axes[0].set_xlabel('Personal Weather Stations (PWS)')
axes[0].set_ylabel('Total Canopy Area (sq. m) * 10^6')
axes[0].grid(True)

# Plotting Mean Canopy Height vs. PWS
sns.lineplot(x='PWS_Value', y='Mean Canopy Height (m)', marker='o', color='green', data=df_canopy, ax = axes[1])
axes[1].set_title('Mean Canopy Height vs. PWS')
axes[1].set_xlabel('Personal Weather Stations (PWS)')
axes[1].set_ylabel('Mean Canopy Height (m)')
axes[1].grid(True)

# Plotting Canopy coverage % vs. PWS
sns.barplot(x='PWS_Value', y='Coverage (%)', hue='PWS_Value', legend=False, palette='cool', data=df_canopy, ax = axes[2])
axes[2].set_title('Canopy Coverage (%) vs. PWS')
axes[2].set_xlabel('Personal Weather Stations (PWS)')
axes[2].set_ylabel('Canopy Coverage (%)')
axes[2].grid(True)

plt.tight_layout()
plt.show()