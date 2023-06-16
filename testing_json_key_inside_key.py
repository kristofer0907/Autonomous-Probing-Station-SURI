import json
import os.path


################ TESTING DICTIONARY IN JSON
voltage_level =0.5
test_list = list()
for i in range(-10,10,2):
    test_list.append(i)

data = {voltage_level:test_list}

file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
file_name = "new_data.json"

actual_file = file_path+file_name

# Read json file
with open(actual_file) as fp:
    listObj = json.load(fp)





print(listObj)

with open(actual_file,"w") as json_file:
    json.dump(listObj, json_file,
              indent = 4,
              separators = (",",": "))
    







