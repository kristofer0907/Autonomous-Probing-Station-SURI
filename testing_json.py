import json
voltage_level =0.5
test_list = list()
for i in range(-10,10,1):
    test_list.append(i)

data = {voltage_level:test_list}
print(data)

file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
file_name = "new_data.json"
file_location = file_path+file_name
print(file_location)
with open(file_location,'w') as json_file:
    json.dump(data,json_file)

# Check if the file exis