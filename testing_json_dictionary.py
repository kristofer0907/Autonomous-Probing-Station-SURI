import json
import os.path


################ TESTING DICTIONARY IN JSON

############USER INPUT############

file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
file_name = "new_data.json"
voltage_min =-0.5
start_voltage = round(voltage_min,1)
steps = 0.1
voltage_max = 0.5
iterations = 3
iteration_for_use = iterations-iterations+1
############SETUP############
actual_file = file_path+file_name

data = {}
while start_voltage <=voltage_max:
    data[round(start_voltage,1)] = {}
    x = 1
    while x <= iterations:
        data[round(start_voltage,1)][x] = ""

        x += 1

    start_voltage = round(start_voltage + steps,1)
    


with open(actual_file,'w') as json_file:
     json.dump(data,json_file,indent = 4)



collected_data1 = [-0.0009556601405622491, -0.0009595047429718876, -0.0009659124136546185, -0.0009607862771084337, -0.0009607862771084337, -0.0009582232088353413, -0.0009595047429718876, -0.00096206781124498, -0.0009595047429718876, -0.0009582232088353413]
collected_data2 = [-0.0009556601405622491, -0.0009595047429718876, -0.0009659124136546185, -0.0009607862771084337, -0.0009607862771084337, -0.0009582232088353413, -0.0009595047429718876, -0.00096206781124498, -0.0009595047429718876, -0.0009582232088353413]
collected_data3 = [-0.0009556601405622491, -0.0009595047429718876, -0.0009659124136546185, -0.0009607862771084337, -0.0009607862771084337, -0.0009582232088353413, -0.0009595047429718876, -0.00096206781124498, -0.0009595047429718876, -0.0009582232088353413]


with open(actual_file,'r') as json_file:
     data = json.load(json_file)


start_voltage = voltage_min
while start_voltage <=voltage_max:
    x = 1
    while x <= iterations:
        data[str(round(start_voltage,1))][str(x)] = collected_data1

        x += 1

    start_voltage = round(start_voltage + steps,1)


print(data)

with open(actual_file,'w') as json_file:
    json.dump(data,json_file,indent =4 )

# data2 = {voltage_level2:test_list2}



# file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
# file_name = "new_data.json"

# actual_file = file_path+file_name

# # with open(actual_file,"w") as json_file:
# #     json.dump(data,json_file,indent = 4)

# if os.path.isfile(actual_file) is False:
#     raise Exception("File not found")


# Read json file
# with open(actual_file) as fp:
#     listObj = json.load(fp)


# print(listObj)
# print(type(listObj))

# listObj.update(data2)

# print(listObj)

# with open(actual_file,"w") as json_file:
#     json.dump(listObj, json_file,
#               indent = 4,
#               separators = (",",": "))
    







