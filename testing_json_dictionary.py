import json
import os.path


################ TESTING DICTIONARY IN JSON

############USER INPUT############

file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
file_name = "new_data.json"
voltage_min =-0.5
start_voltage = voltage_min
steps = 0.1
voltage_max = 0.5
iterations = 3

############COMPUTER WORK############
actual_file = file_path+file_name

data = {}
x = 0
while start_voltage <=voltage_max:
    data[start_voltage] = {}
    while x <= iterations:
        data[start_voltage][iterations] = ""
        x += 1

    start_voltage += steps
    
print(data)

# with open(actual_file,'w') as json_file:
#     json.dump(data,json_file,indent = 4)













# data = {voltage_level:test_list}



# voltage_level2 = 0.6
# test_list2 = list()
# for i in range(-10,10,1):
#     test_list2.append(i)

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
    







