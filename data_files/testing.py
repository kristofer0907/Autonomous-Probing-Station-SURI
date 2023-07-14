import numpy as np
import matplotlib.pyplot as plt

# Data for seven sets
x = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
    [4, 8, 12, 16, 20],
    [5, 10, 15, 20, 25],
    [6, 12, 18, 24, 30],
    [7, 14, 21, 28, 35]
]

y = [
    [6, 7, 8, 9, 10],
    [5, 3, 1, 7, 9],
    [9, 8, 7, 6, 5],
    [15, 12, 9, 6, 3],
    [2, 4, 6, 8, 10],
    [3, 2, 1, 5, 6],
    [8, 6, 4, 2, 10]
]

# Scatter plot with different colors for each data set
plt.figure(figsize=(10, 6))

for i in range(len(x)):
    plt.scatter(x[i], y[i], label=f'Set {i+1}', alpha=0.7)

    # Combine data for linear regression
    x_combined = np.concatenate(x)
    y_combined = np.concatenate(y)

    # Perform linear regression
    fit = np.polyfit(x_combined, y_combined, 1)

    # Create regression line
    regression_line = np.poly1d(fit)

    # Plot regression line
    plt.plot(x_combined, regression_line(x_combined), color='black', linewidth=1.5, linestyle='--')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot with Linear Fit (All Data)')
plt.legend()

plt.show()
