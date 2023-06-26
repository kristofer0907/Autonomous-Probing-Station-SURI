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



# import datashader as ds
# import pandas as pd
# import colorcet as cc
# import json
# import matplotlib.pyplot as plt

# # Load the JSON data from the file
# with open('test6.json', 'r') as file:
#     data = json.load(file)


# # 3 variables: 1. Type of data.     2. Voltage level       3. Iterations

# step = 0.001
# variable = "Current"
# voltage_max = 0.005
# voltage_min = -0.005
# x = voltage_min
# while x != voltage_max:
#     for i in range(1,3):
#         value = data[variable][str(x)][str(i)]
        
#         #plt.scatter(value,current_values)
#     x = round(x+step,3)

# print(len(value))
# print(len(current_values))
# plt.scatter(value,current_values)

# plt.xlabel("Voltage")
# plt.ylabel("Current")
# plt.legend()



# print(value)


# # for i in range(1,3): #Iterations
# #     for data["Current"][str(i)], measurements in data.items():
# #         # Convert the current measurements to a numpy array
# #         current_values = data["Current"][i].items()

# #         # Plot the current measurements
# #         plt.plot(range(1, 11), current_values, marker='o', label=f'Voltage: {data["Current"][str(i)]}')

# # # Add labels and legends to the plot
# # plt.xlabel('Measurement')
# # plt.ylabel('Current')
# # plt.title('Current Measurements for Different Voltage Levels')
# # plt.legend()

# # # Display the plot
# # plt.show()


import matplotlib.pyplot as plt

# Example dictionary
data_dict = {
    -0.05: [0.19, 0.12, 0.19],
    -0.04: [0.19, 0.14, 0.12],
    # Continue adding more key-value pairs here
    # ...
    0.05: [-0.17, -0.12, -0.15]  # Replace value1, value2, and value3 with the actual values
}

# Extract keys and values from the dictionary
keys = list(data_dict.keys())
values = list(data_dict.values())

# Flatten the values list
flattened_values = [item for sublist in values for item in sublist]

# Plot the data
plt.scatter(keys * len(values), flattened_values, marker='o', linestyle='-', color='b')
plt.xlabel('Key')
plt.ylabel('Value')
plt.title('Key-Value Plot')
plt.grid(True)

# Display the plot
plt.show()
