import json
import os.path
voltage_level =0.5
test_list = list()
for i in range(-10,10,2):
    test_list.append(i)




data = {voltage_level:test_list}



voltage_level2 = 0.6
test_list2 = list()
for i in range(-10,10,1):
    test_list2.append(i)

data2 = {voltage_level2:test_list2}



file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
file_name = "new_data.json"

actual_file = file_path+file_name

# with open(actual_file,"w") as json_file:
#     json.dump(data,json_file,indent = 4)

if os.path.isfile(actual_file) is False:
    raise Exception("File not found")


# Read json file
with open(actual_file) as fp:
    listObj = json.load(fp)


print(listObj)
print(type(listObj))

listObj.update(data2)

print(listObj)

with open(actual_file,"w") as json_file:
    json.dump(listObj, json_file,
              indent = 4,
              separators = (",",": "))
    







