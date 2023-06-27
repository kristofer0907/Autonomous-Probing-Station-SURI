# # import time

# # class Test_shit:


# #     def count_zeros_in_float(self,number):
# #         number_str = str(number)

# #         # Initialize a counter for zeros
# #         zeros_count = 0

# #         # Iterate over each character in the string
# #         for char in number_str:
# #             if char == '0':
# #                 zeros_count += 1

# #         return zeros_count
    
# #     def get_zeros(self,min,max,count=0 ):
# #         min = abs(min)       
# #         min = str(min)
# #         if min[count]=="0" or min[count].isdigit()== False:
# #             count += 1
# #             return self.get_zeros(float(min),max,count)    
# #         else:
# #             if type(max)==float:
# #                 self.zeros = count-1
# #                 print(self.zeros)
# #                 return
# #             self.zeros = count
# #             print(self.zeros)
# #             return

# # tester= Test_shit()
# # time_start = time.time()
# # print(tester.count_zeros_in_float(-0.005))
# # print(f"Timer for GBT: {time.time()-time_start}")
# # print(tester.get_zeros(-0.005,0.005))
# # print(f"Timer for me: {time.time()-time_start}")


# # print("  _____            _               _______                      ")
# # print(" |  __ \          | |             |__   __|                     ")
# # print(" | |__) |___   ___| | _____ _ __     | | __ _  __ _  ___ _ __   ")
# # print(" |  _  // _ \ / __| |/ / _ \ '__|    | |/ _` |/ _` |/ _ \ '__|  ")
# # print(" | | \ \ (_) | (__|   <  __/ |       | | (_| | (_| |  __/ |     ")
# # print(" |_|  \_\___/ \___|_|\_\___|_|       |_|\__,_|\__, |\___|_|     ")
# # print("                                              __/ |            ")
# # print("                                             |___/             ")
# # print("   ____                 _         _                             ")
# # print("  / __ \               (_)       | |                            ")
# # print(" | |  | |_ __ ___  __ _ _ _ __   | |__   ___ _ __               ")
# # print(" | |  | | '__/ _ \/ _` | | '_ \  | '_ \ / _ \ '__|              ")
# # print(" | |__| | | |  __/ (_| | | | | | | | | |  __/ |                 ")
# # print("  \____/|_|  \___|\__, |_|_| |_| |_| |_|\___|_|                 ")
# # print("                  __/ |                                         ")
# # print("                 |___/                                          ")
# # print("   ____       _                                                  ")
# # print("  / __ \     | |                                                 ")
# # print(" | |  | |_ __| | __ _ _ __   __ _  __ _  ___ _ __                ")
# # print(" | |  | | '__| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|               ")
# # print(" | |__| | |  | | (_| | | | | (_| | (_| |  __/ |                  ")
# # print("  \____/|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|                  ")
# # print("                                  __/ |                         ")
# # print("                                                                 ")



import datashader as ds
import pandas as pd
import colorcet as cc
import json
import matplotlib.pyplot as plt
import numpy as np
# Load the JSON data from the file
with open('test10.json', 'r') as file:
    data = json.load(file)


# # 3 variables: 1. Type of data.     2. Voltage level       3. Iterations

step = 0.1
variable = "Current"
voltage_max = 1.0
voltage_min = -1.0
x = voltage_min
GAIN = 1
empty_dict = {}
while x <= voltage_max:
    for i in range(1,2):
        value = data[variable][str(x)][str(i)]
        if i == 2:
            empty_dict[x] +=[v * GAIN for v in value]

        empty_dict[x]=[v * GAIN for v in value]
        #plt.scatter(value,current_values)
    x = round(x+step,3)

keys = list(empty_dict.keys())
values = list(empty_dict.values())

# Flatten the values list
flattened_values = [item for sublist in values for item in sublist]
x_coords = []
for key, val in empty_dict.items():
    x_coords.extend([key] * len(val))




x_coords = np.array(x_coords)
flattened_values = np.array(flattened_values)

# Calculate G/G_0 values
G_G0_values = flattened_values[0] / x_coords[0] / (7.77e-5)
print(G_G0_values)


slope, intercept = np.polyfit(x_coords, flattened_values, 1)

# Generate the predicted y-values based on the line equation
y_fit = slope * np.array(x_coords) + intercept


# Plot the data as a scatter plot
plt.scatter(x_coords, flattened_values, marker='o',facecolors="none" ,edgecolors='b')


plt.plot(x_coords, y_fit, color='r', label='Line of Best Fit')




plt.xlabel('Voltage')
plt.ylabel('Current')
plt.title('I-V Plot')
plt.grid(True)

# Display the plot
plt.show()

# for i in range(1,3): #Iterations
#     for data["Current"][str(i)], measurements in data.items():
#         # Convert the current measurements to a numpy array
#         current_values = data["Current"][i].items()

#         # Plot the current measurements
       

# import matplotlib.pyplot as plt

# # Example dictionary
# empty_dict = {
#     -0.05: [0.19, 0.12, 0.19],
#     -0.04: [0.19, 0.14, 0.12],
#     # Continue adding more key-value pairs here
#     # ...
#     0.05: [-0.17, -0.12, -0.15]  # Replace value1, value2, and value3 with the actual values
# }

# # Extract keys and values from the dictionary
# keys = list(empty_dict.keys())
# values = list(empty_dict.values())

# # Flatten the values list
# flattened_values = [item for sublist in values for item in sublist]
# x_coords = []
# for key, val in empty_dict.items():
#     x_coords.extend([key] * len(val))

# # Plot the data as a scatter plot
# plt.scatter(x_coords, flattened_values, marker='o', color='b')
# # Plot the data
# plt.xlabel('Voltage')
# plt.ylabel('Current')
# plt.title('I-V Plot')
# plt.grid(True)

# # Display the plot
# plt.show()
