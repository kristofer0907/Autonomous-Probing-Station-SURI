import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math
import json
import os

class DAQ:
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
        zeros_count = 0
        for char in number_str:
            if char == '0':
                zeros_count += 1
        self.zeros = zeros_count+2
        return 
    
    def create_correct_order(self,current_number):
        pass

    def plotter(self,iterations):
        with open(self.actual_file, 'r') as file:
            data = json.load(file)
        x = self.start_voltage
        print(data)
        empty_dict = {}
        area1 = []
        area2 = []
        area3 = []
        area4 = []
        # for i in data[variable]:
        #     print(i.value())

        first_number = 0
        second_number = 1

        while x <= self.start_voltage_max:
            for i in range(1,iterations+1):
                if x>=0:
                    area1.append(data[variable][str(x)][str(i)][first_number]*GAIN)
                    area2.append(data[variable][str(x)][str(i)][second_number]*GAIN)
                elif x<0:
                    area3.append(data[variable][str(x)][str(i)][first_number]*GAIN)
                    area4.append(data[variable][str(x)][str(i)][second_number]*GAIN)
                x = round(x+self.steps,self.zeros)
        
        whole_area = area1+area2+area3+area4





        #         #if i == 2:
        #             #empty_dict[x] +=[v * GAIN for v in value] #TODO Account for more iteratations
        #         empty_dict[x]=[v * GAIN for v in value]
        #     x = round(x+self.steps,self.zeros)
        

        # keys = list(empty_dict.keys())
        # values = list(empty_dict.values())

        # # Flatten the values list
        # flattened_values = [item for sublist in values for item in sublist]
        # x_coords = []
        # for key, val in empty_dict.items():
        #     x_coords.extend([key] * len(val))

        y_coords = np.array(whole_area) # Voltage input
        x_coords = np.linspace(self.start_voltage,self.start_voltage_max,len(whole_area))
        

        # flattened_values = np.array(flattened_values) #Voltage measured
        # junction_current = flattened_values

        # Calculate G/G_0 values
        # G_G0_values = flattened_values[0] / x_coords[0] / (7.77e-5)
        # print(G_G0_values)


        slope, intercept = np.polyfit(x_coords, y_coords, 1)
        y_fit = slope * np.array(x_coords) + intercept
        plt.scatter(x_coords, y_coords, marker='o',facecolors="none" ,edgecolors='b')
        plt.plot(x_coords, y_fit, color='r', label='Line of Best Fit')
        plt.xlabel('Voltage')
        plt.ylabel('Current')
        plt.title('I-V Plot')
        plt.grid(True)
        plt.show()
    

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
        #### Take care of number going from start to max ####
        while start_voltage <=voltage_max:
            data[variable][round(start_voltage,self.zeros)] = {}
            x = 1
            while x <= iterations:
                data[variable][round(start_voltage,self.zeros)][x] = []

                x += 1

            start_voltage = round(start_voltage + steps,self.zeros)
        # #### Take care of number going from max to min ####
        # tart_voltage = round(start_voltage - steps,self.zeros)
        # while start_voltage>= voltage_min:
        #     data[variable][round(start_voltage,self.zeros)] = {}
        #     x = 1
        #     while x <= iterations:
        #         data[variable][round(start_voltage,self.zeros)][x] = []

        #         x += 1

        #     start_voltage = round(start_voltage - steps,self.zeros)

        # #### Take care of number going from min to start #### 
        # while start_voltage<=0:
        #     data[variable][round(start_voltage,self.zeros)] = {}
        #     x = 1
        #     while x <= iterations:
        #         data[variable][round(start_voltage,self.zeros)][x] = ""

        #         x += 1

        #     start_voltage = round(start_voltage + steps,self.zeros)



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
        try:#If there is already a value in the measured values list
            data[variable][str(round(current_voltage,self.zeros))][str(iteration)][0]
            data[variable][str(round(current_voltage,self.zeros))][str(iteration)][[1]] = collected_data
        except:#If there is not already a value in the measured values list
            data[variable][str(round(current_voltage,self.zeros))][str(iteration)].append(collected_data)

        # while self.start_voltage <=self.start_voltage_max:
        #     x = 1
        #     while x <= iterations:
        #         data[str(round(self.start_voltage,2))][str(x)] = collected_data

        #         x += 1
        
        #     self.start_voltage = round(self.start_voltage + self.steps,2)

        with open(self.actual_file,'w') as json_file:
            json.dump(data,json_file,indent =4 )


    def verify(self,string,name):
        if string == "channel output":
            try:
                with nidaqmx.Task() as task:
                    task.ao_channels.add_ao_voltage_chan(name)
                return True
            except nidaqmx.DaqError:
                return False
        elif string == "channel input":
            try:
                with nidaqmx.Task() as task:
                    task.ai_channels.add_ai_voltage_chan(name)
                    
                return True
            except nidaqmx.DaqError:
                return False
            
        elif string == "number":
            pass
     

############## INPUTS ############## 

variable = "Current"
############## UI ############## 
print('WELCOME TO THE AUTO-PROBER2023, please select one of the following options: ')


class UI:
    
    def start(self):
                
        print(" 1. I-V characteristics")
        print(" 2. I-t characteristics")
        print(" 3. Calibration")
        users_choice = input("Input: ")
        if users_choice == "1":
            Run_everything().anything(False)
        elif users_choice == "2":
            Run_everything().something()
            
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
        analog_input_channel = input("Analog input channel: ")  # Replace with the appropriate channel name for your setup
        verify_input_channel = DAQ().verify("channel input",analog_input_channel)
        if verify_input_channel == False:
            print("The name given for the analog input is incorrect, try again")
            self.get_info_for_DAQ()
        analog_output_channel = input("Analog output channel: ")
        verify_output_channel = DAQ().verify("channel output",analog_output_channel)
        if verify_output_channel ==False:    
            print("The name given for the analog output is incorrect, try again")
            self.get_info_for_DAQ()
        file_name = input("Filename: ") 
        file_name = file_name+".json"# User should select the filename, said filename will be used in the future for 
        file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
        try:
            SAMPLE_AMOUNT = int(input("Sample amount: "))
            SAMPLE_RATE = int(input("Sample rate [Hz]: "))
        except:
            print("The sample amount and sample rate can only be whole numbers")
            self.get_info_for_DAQ()
        VOLTAGE_MIN = float(input("Voltage minimum: "))
        VOLTAGE_MAX = float(input("Voltage max: "))
        STEPS = float(input("Incremental steps between voltages: "))
        ITERATIVES = int(input("Iteratives: "))
        GAIN = float(input("Gain: "))
        print("Would you like to continue(yes/no)?")
        selection = input("Input: ")
        if selection == "yes":
            pass
        elif selection =="no":
            self.start()
            #self.get_info_for_DAQ()
        else:
            print("Please enter either yes or no")

        return analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN

    
    def get_info_i_t(self):
        analog_input_channel = input("Analog input channel: ")  # Replace with the appropriate channel name for your setup
        verify_input_channel = DAQ().verify("channel input",analog_input_channel)
        if verify_input_channel == False:
            print("The name given for the analog input is incorrect, try again")
            self.get_info_for_DAQ()
        file_name = input("Filename: ") 
        file_name = file_name+".json"# User should select the filename, said filename will be used in the future for 
        file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
       
        desired_voltage = float(input("Enter the desired voltage level in volts: "))
        desired_time = float(input("Enter the desired measurement time in seconds: "))
        num_samples = int(input("Enter the number of samples to acquire: "))

        print("Would you like to continue(yes/no)?")
        selection = input("Input: ")
        if selection == "yes":
            pass
        elif selection =="no":
            self.start()
            #self.get_info_for_DAQ()
        else:
            print("Please enter either yes or no")
        return desired_voltage,desired_time,num_samples,file_name,file_path,analog_input_channel
    def ending(self):
        print("Data has been sucessfully collected, select one of the following options: ")
        print(" 1. Run again with same constraints and conditions")
        print(" 2. Run with different constraints and conditions")
        print(" 3. Return to main menu")
        print(" 4. Quit program")
        users_end = input(" Input: ")
        if users_end == "1":
            boolean = True
            Run_everything().anything(boolean)
        elif users_end == "2":
            boolean = None
            Run_everything().anything(boolean)
        elif users_end == "3":
            self.start()
        elif users_end == "4":
            pass
        else:
            print("Please select an available option")
            time.sleep(1)
            self.ending()


############## CALLING MAIN ############## 

class Run_everything():
    def __init__(self):
        user_interface=  UI()
        self.user_interface = user_interface



    def anything(self,boolean): ### For I-V option
       
        


        if boolean == False:
            global analog_input_channel, analog_output_channel, SAMPLE_AMOUNT, SAMPLE_RATE, file_name, file_path, VOLTAGE_MIN, VOLTAGE_MAX, STEPS, ITERATIVES,GAIN
            analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN= self.user_interface.get_info_for_DAQ()

        elif boolean == True:
            pass
        else:
            analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN= self.user_interface.get_info_for_DAQ()
  

        main = DAQ()
        
        logical_check = main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path)
        if logical_check == str: #Means it doesnt exist already
            pass
        elif logical_check == int: ### Means the file exists already
            new_name_file= self.user_interface.file_exists()
            if new_name_file == None:
                main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path)
            else:
                main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,new_name_file,file_path)

        start_time = time.time()
        main.count_zeros_in_float(VOLTAGE_MIN)
        voltage_levels = main.create_interval(VOLTAGE_MIN,VOLTAGE_MAX,STEPS) # TODO: Make interval muteable for user
        main.setup(voltage_levels,STEPS,variable,ITERATIVES)

        voltage_min = -0.1
        voltage_max = 0.1
        voltage_step = 0.01

        x = 1
        while x <= ITERATIVES:    
            with nidaqmx.Task() as output_task:
                output_task.ao_channels.add_ao_voltage_chan("cDAQ1Mod1/ao0", min_val=voltage_min, max_val=voltage_max)

                # Create a task for analog input
                with nidaqmx.Task() as input_task:
                    input_task.ai_channels.add_ai_voltage_chan("cDAQ1Mod2/ai0")

                    # Set initial output voltage to 0V
                    output_task.write(0)

                    # Increase voltage to max
                    for voltage in range(0, int(voltage_max * 100) + 1, int(voltage_step * 100)):
                        voltage /= 100.0
                        output_task.write(voltage)
                        input_voltage = input_task.read()
                        #print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")
                        main.storing(voltage,input_voltage,x,variable)

                    # Decrease voltage to min
                    for voltage in range(int(voltage_max * 100), int(voltage_min * 100) - 1, -int(voltage_step * 100)):
                        voltage /= 100.0
                        output_task.write(voltage)
                        input_voltage = input_task.read()
                        #print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")
                        main.storing(voltage,input_voltage,x,variable)
                    # Traverse back up to 0V
                    for voltage in range(int(voltage_min * 100), int(voltage_step), int(voltage_step * 100)):
                        voltage /= 100.0
                        output_task.write(voltage)
                        input_voltage = input_task.read()
                        #print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")
                        main.storing(voltage,input_voltage,x,variable)
                    x += 1

        # for voltage_level in voltage_levels:
        #     if voltage_level == -0.0:
        #         voltage_level =0.0
            # x = 1
            # while x <= ITERATIVES:    
            #     main.set_analog_output(analog_output_channel,voltage_level,SAMPLE_AMOUNT)
              
            #     #current_reading,current_time = main.read_current(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
            #     voltage_reading,voltage_time = main.read_voltage(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
            #     #main.storing(voltage_level,current_reading,x,variable)
            #             # variable = "Voltage"
            #             # main.setup(voltage_levels,STEPS,variable,ITERATIVES)
            #     main.storing(voltage_level,voltage_reading,x,variable)
                
                        
               
        end_time = time.time()-start_time
        print("")
        print(f"Time it took to collect data: {end_time}")
        print("")
        main.plotter(ITERATIVES)
        self.user_interface.ending()
        

    def something(self):
        desired_voltage,desired_time,num_samples,analog_output,analog_input= self.user_interface.get_info_i_t()
        with nidaqmx.Task() as output_task:
            # Add an analog output voltage channel
            output_task.ao_channels.add_ao_voltage_chan(analog_output)  # Replace with your channel name

            # Configure the desired voltage level
            output_task.write(desired_voltage)

            # Create a task for analog input
            with nidaqmx.Task() as input_task:
                # Add an analog input voltage channel
                input_task.ai_channels.add_ai_voltage_chan(analog_input)  # Replace with your channel name

                # Configure timing settings
                sample_rate = num_samples / desired_time  # Set the sample rate based on the desired time and number of samples
                input_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

                # Read the voltage data
                voltage_data = input_task.read(number_of_samples_per_channel=num_samples, timeout=float("1000"))

        # Calculate the current from the voltage data
        current_data = [10 * voltage for voltage in voltage_data]

        # Generate the time axis for the plot
        time = np.linspace(0, desired_time, len(current_data))

        # Plot the current measurements over time
        plt.plot(time, current_data)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (A)')
        plt.title('Current vs. Time')
        plt.grid(True)
        plt.show()


boolean = False
UI().start()
