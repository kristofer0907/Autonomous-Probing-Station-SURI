import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math
import json
import os
import serial
from tabulate import tabulate

# variable = "I-V data"
# file_name = "testing50"
# actual_file = file_name+".json"
# pair = 1
# identifier = f"Pair number: {pair}"
# with open(actual_file,'r+') as file:
#                             # First we load existing data into a dict.
#     file_data = json.load(file)
#     data = file_data[variable][0][identifier]



# # Print the data table



import json

variable = "I-V data"
file_name = "testing60"
actual_file = file_name + ".json"
pair = 2
identifier = f"Pair number: {pair}"

# Load data from the JSON file
with open(actual_file, 'r+') as file:
    file_data = json.load(file)

# Function to find the data for a specific pair number
def get_pair_data(data_list, pair_number):
    for item in data_list:
        if f"Pair number: {pair_number}" in item:
            return item[f"Pair number: {pair_number}"]

    return None

# Get data for the specified pair number
data = get_pair_data(file_data[variable], pair)

table_data = []
for idx, val in enumerate(data['1']['input']):
    table_data.append([val, data['1']['output'][idx]])

input_data = data['1']['input']
output_data = data['1']['output']
headers = ['Input', 'Output']
print(tabulate(table_data, headers=headers))

plt.scatter(output_data, input_data,marker = "o",label = "Data") 
plt.xlabel('Voltage')
plt.ylabel('Current')
plt.title(f'I-V for Pair number {2}')
plt.legend()
plt.grid(True)
plt.show()
# Check if the data was found and print the output and input values
