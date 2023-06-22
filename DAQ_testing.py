import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math
import json
import os



class DAQ:
    def __init__(self,analog_input_channel,analog_output_channel):
        self.analog_input_channel =analog_input_channel
        self.analog_output_channel = analog_output_channel

    def get_user_parameters(self,sample_amount,sample_rate,file_name,file_path):
        self.sample_amount = sample_amount
        self.sample_rate = sample_rate
        self.file_name = file_name
        if self.search_file(file_path,self.file_name) == None:
            return str
        else:
            return int
    def count_zeros_in_float(self,number):
        number_str = str(number)

        # Initialize a counter for zeros
        zeros_count = 0

        # Iterate over each character in the string
        for char in number_str:
            if char == '0':
                zeros_count += 1
        self.zeros = zeros_count
        return 
    

    

    def create_interval(self,start, end, step):
        interval_list = []
        num = start
        while round(num,self.zeros) <= end:
            interval_list.append(round(num,self.zeros))
            num += step
        return interval_list


    def search_file(self,folder_path, file_name):
        for root, dirs, files in os.walk(folder_path):
            if file_name in files:
                return os.path.join(root, file_name)
        return None

# # Usage example
# folder_path = '/path/to/folder'
# file_name = 'example.txt'
# result = search_file(folder_path, file_name)

# if result:
#     print(f"The file '{file_name}' exists in the folder: {result}")
# else:
#     print(f"The file '{file_name}' does not exist in the folder.")



    def setup(self,interval,steps,variable,iterations):
        self.steps = steps        
        file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
        voltage_min = min(interval)
        start_voltage = voltage_min
        self.start_voltage = start_voltage
        voltage_max = max(interval)
        self.start_voltage_max = voltage_max
        #variable = str(variable)
        
        ############SETUP############
       
        


        actual_file = file_path+self.file_name
        self.actual_file = actual_file

        data = {}
       

        data[variable] = {}
        while start_voltage <=voltage_max:
            data[variable][round(start_voltage,self.zeros)] = {}
            x = 1
            while x <= iterations:
                data[variable][round(start_voltage,self.zeros)][x] = ""

                x += 1

            start_voltage = round(start_voltage + steps,self.zeros)


        with open(actual_file,'w') as json_file:
            json.dump(data,json_file,indent = 4)

    def set_analog_output(self,analog_input_channel,voltage_level,num_samples):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(analog_input_channel)
            #task.timing.cfg_samp_clk_timing(rate=rate,samps_per_chan=num_samples)
            task.write(voltage_level)

    def read_current(self,analog_input_channel,sample_amount,sample_rate):    
        with nidaqmx.Task() as task:
            #task.wait_until_done(timeout=1000)
            task.wait_until_done = float(sample_amount/sample_rate+1)

            task.ai_channels.add_ai_current_chan(analog_input_channel)
            task.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan=sample_amount)
            #task.start()
            start_time= time.time()
            data = task.read(number_of_samples_per_channel= SAMPLE_AMOUNT,timeout=float("1000"))        
            elapsed_time = time.time()-start_time
            time_array = np.linspace(0, elapsed_time, sample_amount)

            return data,time_array
            #task.ai_channels.add_ai_current_rms_chan(analog_input_channel)

    def read_voltage(self,analog_input_channel,SAMPLE_AMOUNT,sample_rate):    
        with nidaqmx.Task() as task:
            task.wait_until_done = float(SAMPLE_AMOUNT/sample_rate+1)

            task.ai_channels.add_ai_voltage_chan(analog_input_channel)
            task.timing.cfg_samp_clk_timing(sample_rate,samps_per_chan=SAMPLE_AMOUNT)
            task.start()
            start_time = time.perf_counter()
            data = task.read(number_of_samples_per_channel= SAMPLE_AMOUNT,timeout=float("1000"))
            end_time = time.perf_counter()
            elapsed_time= end_time-start_time
            time_array = np.linspace(0,elapsed_time,SAMPLE_AMOUNT)        
            return data, time_array


    def storing(self,current_voltage,collected_data,iteration,variable):
        '''Keep the data acquired in a dict'''        
        variable = str(variable)
        with open(self.actual_file,'r') as json_file:
            data = json.load(json_file)
        data[variable][str(round(current_voltage,self.zeros))][str(iteration)] = collected_data
        # while self.start_voltage <=self.start_voltage_max:
        #     x = 1
        #     while x <= iterations:
        #         data[str(round(self.start_voltage,2))][str(x)] = collected_data

        #         x += 1

        #     self.start_voltage = round(self.start_voltage + self.steps,2)

        with open(self.actual_file,'w') as json_file:
            json.dump(data,json_file,indent =4 )


        

    def plotter(self,x,y):
        plt.plot(x,y)
        plt.show()



############## INPUTS ############## 
file_name = "test6.json" # User should select the filename, said filename will be used in the future for 
file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"

analog_input_channel = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
analog_output_channel = "cDAQ1Mod1/ao0"
SAMPLE_AMOUNT = 10
SAMPLE_RATE = 1000
VOLTAGE_MIN = -0.005
VOLTAGE_MAX = 0.005
STEPS = 0.001
ITERATIVES = 2
variable = "Current"
############## UI ############## 
print('WELCOME TO THE AUTO-PROBER2023 , please select one of the following options: ')
# file_name = input("Filename: ") 
# file_name = file_name+".json"# User should select the filename, said filename will be used in the future for 
# file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"

# start_time = time.time()
# analog_input_channel = input("Analog input channel: ")  # Replace with the appropriate channel name for your setup
# analog_output_channel = input("Analog output channel: ")

# SAMPLE_AMOUNT = int(input("Sample amount: "))
# SAMPLE_RATE = int(input("Sample rate [Hz]: "))
# VOLTAGE_MIN = float(input("Voltage minimum: "))
# VOLTAGE_MAX = float(input("Voltage max: "))
# STEPS = float(input("Incremental steps between voltages: "))
# ITERATIVES = int(input("Iteratives: "))




############## CALLING MAIN ############## 

class UI:
    
    def start(self):
                
        print(" 1. I-V characteristics")
        print(" 2. I-t characteristics")
        print(" 3. Calibration")
        users_choice = input("  Input:")

        if users_choice == "1":
            return(self.get_info_for_DAQ())
        elif users_choice == "2":
            pass
        elif users_choice == "3":
            pass
        else:
            print("Please select an available option")
            time.sleep(1)
            self.start()
    def file_exists(self):
        print("The file you have asked to write in seems to already exist, please select one of the options below:")
        print(" 1. Overwrite pre-existing file")
        print(" 2. Select a new name")
        new_or_not =input(" Input: ")
        if new_or_not == "2":
            new_name_file = input("Please submit a new name for a file: ")
            new_name_file = new_name_file+".json"
            return new_name_file
        elif new_or_not =="1":
            return
        else:
            print("Please select an available option")
            time.sleep(1)
            self.file_exists()
            #TODO make this into a function or something so that its more 
            # easily possible to make the user start over again

    def get_info_for_DAQ(self):
        file_name = input("Filename: ") 
        file_name = file_name+".json"# User should select the filename, said filename will be used in the future for 
        file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
        analog_input_channel = input("Analog input channel: ")  # Replace with the appropriate channel name for your setup
        analog_output_channel = input("Analog output channel: ")
        SAMPLE_AMOUNT = int(input("Sample amount: "))
        SAMPLE_RATE = int(input("Sample rate [Hz]: "))
        VOLTAGE_MIN = float(input("Voltage minimum: "))
        VOLTAGE_MAX = float(input("Voltage max: "))
        STEPS = float(input("Incremental steps between voltages: "))
        ITERATIVES = int(input("Iteratives: "))
        return analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES





user_interface = UI()
analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES= user_interface.start()
        
main = DAQ(analog_input_channel,analog_output_channel)
logical_check = main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path)
if logical_check == str: #Means it doesnt exist already
    pass
elif logical_check == int: ### Means the file exists already
    new_name_file= user_interface.file_exists()
    if new_name_file == None:
        main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path)
    else:
        main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,new_name_file,file_path)

start_time = time.time()
main.count_zeros_in_float(VOLTAGE_MIN)
voltage_levels = main.create_interval(VOLTAGE_MIN,VOLTAGE_MAX,STEPS) # TODO: Make interval muteable for user
main.setup(voltage_levels,STEPS,variable,ITERATIVES)

for voltage_level in voltage_levels:
    x = 1
    while x <= ITERATIVES:    
        main.set_analog_output(analog_output_channel,voltage_level,SAMPLE_AMOUNT)
        current_reading,current_time = main.read_current(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
                #voltage_reading,voltage_time = main.read_voltage(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
        main.storing(voltage_level,current_reading,x,variable)
                # variable = "Voltage"
                # main.setup(voltage_levels,STEPS,variable,ITERATIVES)
                # main.storing(voltage_level,voltage_reading,x,variable)
                #main.plotter(current_time,current_reading)
                
        x += 1
end_time = time.time()-start_time
print(end_time)

# Get user to state how many iterations, the voltage interval, the step in between, and the filename


# ----------------- >>>>>>>>>>>
# ----------------- >>>>>>>>>>>>>>
# ----------------- >>>>>>>>>>>

# Create a json file with the amount of iterations and the voltage interval

# ----------------- >>>>>>>>>>>
# ----------------- >>>>>>>>>>>>>>
# ----------------- >>>>>>>>>>>

# Take measurements for each iteration, store them in the json file 


