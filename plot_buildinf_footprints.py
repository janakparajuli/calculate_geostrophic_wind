# Plots building footprints

import pandas as pd
import matplotlib.pyplot as plt

# Sample data creation, replace this with your actual data load method
data = {
    'PWS': ['PWS20', 'PWS40', 'PWS60', 'PWS80', 'PWS100', 'PWS150', 'PWS200'],
    'Total Footprint Area (sq. m)': [132718.424, 464189.275, 1008682.0307, 1757363.5528, 2647837.5403, 5633673.8242, 9522654.4299],
    'Mean Building Height (m)': [9.127, 9.084, 9.009, 9.025, 9.008, 9.018, 9.007],
    'Coverage (%)': [13.49, 11.91, 11.62, 11.49, 11.18, 10.76, 10.40]
}

df = pd.DataFrame(data)

# Convert PWS to a numeric value for easier plotting
df['PWS_Value'] = df['PWS'].str.extract('(\d+)').astype(int)

# Plotting Total Footprint Area vs PWS
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.plot(df['PWS_Value'], df['Total Footprint Area (sq. m)'], marker='o')
plt.title('Total Footprint Area vs PWS')
plt.xlabel('Personal Weather System')
plt.ylabel('Total Footprint Area (sq. m) * 10^6')

# Plotting Mean Building Height vs PWS
plt.subplot(1, 3, 2)
plt.plot(df['PWS_Value'], df['Mean Building Height (m)'], marker='o', color='red')
plt.title('Mean Building Height vs PWS')
plt.xlabel('Personal Weather System')
plt.ylabel('Mean Building Height (m)')

# Plotting Coverage vs PWS
plt.subplot(1, 3, 3)
plt.plot(df['PWS_Value'], df['Coverage (%)'], marker='o', color='green')
plt.title('Coverage vs PWS')
plt.xlabel('Personal Weather System')
plt.ylabel('Coverage (%)')

plt.tight_layout()
plt.show()
