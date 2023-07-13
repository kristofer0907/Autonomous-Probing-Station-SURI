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

    def plotter(self,iterations,interval):
        with open(self.actual_file, 'r') as file:
            data = json.load(file)
        x = self.start_voltage
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
        

        
        area2.reverse()
        area3.reverse()

        main_interval = np.array(interval)

        min_value = np.min(main_interval)
        max_value = np.max(main_interval)

        # Split the main interval into two sub-intervals
        interval4 = list(main_interval[main_interval <= 0])
        interval1 = list(main_interval[main_interval >= 0])
        interval4 = interval4[:-1]
        interval3 = interval4[::-1]
        interval2 = interval1[::-1]
        #interval3 = interval3[1:]        
        # interval1 =  [0.0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
        # interval2= [0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.01,0.0]
        # interval3= [-0.01,-0.02,-0.03,-0.04,-0.05,-0.06,-0.07,-0.08,-0.09,-0.1]
        # interval4= [-0.1,-0.09,-0.08,-0.07,-0.06,-0.05,-0.04,-0.03,-0.02,-0.01]
        plt.scatter(interval1,area1,label ="Area 1",marker="o") 
        plt.scatter(interval2,area2,label ="Area 2",marker="x")
        plt.scatter(interval3,area3,label ="Area 3",marker="o")
        plt.scatter(interval4,area4,label ="Area 4",marker="x")
        plt.xlabel('Voltage')
        plt.ylabel('Current')
        plt.title('I-V Plot')
        plt.legend()
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
        
        ############SETUP############
       
    

        actual_file = file_path+self.file_name
        self.actual_file = actual_file

        data = {}
        data[variable] = []
        with open(actual_file,'w') as json_file:
            json.dump(data,json_file,indent = 4)

        #### Take care of number going from start to max ####
        # while start_voltage <=voltage_max:
        #     data[variable][round(start_voltage,self.zeros)] = {}
        #     x = 1
        #     while x <= iterations:
        #         data[variable][round(start_voltage,self.zeros)][x] = []

        #         x += 1

        #     start_voltage = round(start_voltage + steps,self.zeros)
        


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
    def write_json(self,new_data, filename,boolean):
        if boolean == False:
            data = {}
            
            data["I-t data"] = []
            with open(filename,'w') as json_file:
                json.dump(data,json_file,indent = 4)
            boolean = True
            return
          
        elif boolean == True:
            with open(filename,'r+') as file:
            # First we load existing data into a dict.
                file_data = json.load(file)

                # Join new_data with file_data inside emp_details
                file_data["I-t data"].append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
    
    # python object to be appended

############## INPUTS ############## 

variable = "I-V data"
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
        while True:
            analog_input_channel = input("Analog input channel: ")
            verify_input_channel = DAQ().verify("channel input", analog_input_channel)
            if verify_input_channel:
                break
            else:
                print("The name given for the analog input is incorrect, try again")

        while True:
            analog_output_channel = input("Analog output channel: ")
            verify_output_channel = DAQ().verify("channel output", analog_output_channel)
            if verify_output_channel:
                break
            else:
                print("The name given for the analog output is incorrect, try again")

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
        number_pairs = int(input("How many pairs of devices are on the micro-chip: "))
        print("Would you like to continue(yes/no)?")
        selection = input("Input: ")
        if selection == "yes":
            pass
        elif selection =="no":
            self.start()
            #self.get_info_for_DAQ()
        else:
            print("Please enter either yes or no")

        return analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN,number_pairs

    
    def get_info_i_t(self):
        while True:
            analog_input_channel = input("Analog input channel: ")
            verify_input_channel = DAQ().verify("channel input", analog_input_channel)
            if verify_input_channel:
                break
            else:
                print("The name given for the analog input is incorrect, try again")

        while True:
            analog_output_channel = input("Analog output channel: ")
            verify_output_channel = DAQ().verify("channel output", analog_output_channel)
            if verify_output_channel:
                break
            else:
                print("The name given for the analog output is incorrect, try again")

        file_name = input("Filename: ") 
        file_name = file_name+".json"# User should select the filename, said filename will be used in the future for 
        file_path = r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
        pairs_of_devices = int(input("Enter the amount of pairs of devices on the chip: "))
        desired_voltage = float(input("Enter the desired voltage level in volts: "))
        desired_time = float(input("Enter the desired measurement time in seconds: "))
        num_samples = int(input("Enter the number of samples to acquire: "))
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
        return desired_voltage,desired_time,num_samples,file_name,file_path,analog_input_channel,analog_output_channel,GAIN,pairs_of_devices
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
            global analog_input_channel, analog_output_channel, SAMPLE_AMOUNT, SAMPLE_RATE, file_name, file_path, VOLTAGE_MIN, VOLTAGE_MAX, STEPS, ITERATIVES,GAIN,number_pairs
            analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN,number_pairs= self.user_interface.get_info_for_DAQ()

        elif boolean == True:
            pass
        else:
            analog_input_channel,analog_output_channel,SAMPLE_AMOUNT,SAMPLE_RATE,file_name,file_path,VOLTAGE_MIN,VOLTAGE_MAX,STEPS,ITERATIVES,GAIN,number_pairs= self.user_interface.get_info_for_DAQ()
  

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
        
        voltage_min = VOLTAGE_MIN
        voltage_max = VOLTAGE_MAX
        voltage_step = STEPS
        
        data = dict()
        #data[variable] = {}
        x = 1
        number = 1
        number_pair = f"Pair number: {number}"
        file_name = file_path+file_name
        plt.ion()

        # Creating subplot and figure
        fig = plt.figure()
        ax = fig.add_subplot(111)
        scatter = None
        while x <= ITERATIVES:  
            input_voltage_list = []
            output_voltage_list = []
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
                        input_voltage_list.append(input_voltage)
                        output_voltage_list.append(voltage)
                        #main.storing(voltage,input_voltage,x,variable)

                    # Decrease voltage to min
                    for voltage in range(int(voltage_max * 100), int(voltage_min * 100) - 1, -int(voltage_step * 100)):
                        voltage /= 100.0
                        output_task.write(voltage)
                        input_voltage = input_task.read()
                        input_voltage_list.append(input_voltage)
                        output_voltage_list.append(voltage)
                        #main.storing(voltage,input_voltage,x,variable)
                    # Traverse back up to 0V
                    for voltage in range(int(voltage_min * 100), int(voltage_step), int(voltage_step * 100)):
                        voltage /= 100.0
                        output_task.write(voltage)
                        input_voltage = input_task.read()
                        input_voltage_list.append(input_voltage)
                        output_voltage_list.append(voltage)
                        #main.storing(voltage,input_voltage,x,variable)
                    input_voltage_list = [GAIN * voltage for voltage in input_voltage_list]
                    data[number_pair]={x:{"output": output_voltage_list, "input": input_voltage_list}}
                                    
                    if x == 1:
                        # Create scatter plot for the first iteration
                        scatter = ax.scatter(output_voltage_list, input_voltage_list, label=f"Iteration {x}")
                        plt.xlabel('Voltage')
                        plt.ylabel('Current')
                        plt.title(f'I-V for Pair number {number_pair}')
                        plt.legend()
                        plt.grid(True)
                        plt.show()

                    else:
                        # Update the data of the scatter plot
                        scatter.set_offsets(np.column_stack((output_voltage_list, input_voltage_list)))
                        

                    color = plt.cm.viridis(x / ITERATIVES)
                    scatter.set_facecolor(color)

                    # Add a legend entry for the current iteration
                    scatter.set_label(f"Iteration {x+1}")

                    # Redraw the figure and pause
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    time.sleep(0.1)
                    x += 1
                    new_data = data


                   
                   
                    # plt.scatter(output_voltage_list,input_voltage_list,label =f"iterative: {x}") 

                    # slope, intercept = np.polyfit(output_voltage_list, input_voltage_list, 1)

                    # # Generate the line using the slope and intercept
                    # line = slope * np.array(output_voltage_list) + intercept

                    # # Plot the linear fit line
                    # plt.plot(output_voltage_list, line, label="Linear Fit", color="red")
                    

                  
                    # x += 1

                    with open(file_name,'r+') as file:
                        # First we load existing data into a dict.
                        file_data = json.load(file)

                        # Join new_data with file_data inside emp_details
                        file_data[variable].append(new_data)
                        # Sets file's current position at offset.
                        file.seek(0)
                        # convert back to json.
                        json.dump(file_data, file, indent = 4)




        number +=1 
            #res = dict(zip(output_voltage_list,input_voltage_list))
            # if number_pair not in data:
            #     data[number_pair] = {}
            # else:
            #     data[number_pair][x] = res
                    

        end_time = time.time()-start_time
        print("")
        print(f"Time it took to collect data: {end_time}")
        print("")
            


            
            #main.plotter(ITERATIVES,voltage_levels)
        self.user_interface.ending()
        

    def something(self):
        desired_voltage,desired_time,num_samples,file_name,file_path,analog_input,analog_output,GAIN,pairs_devices=  self.user_interface.get_info_i_t()
        boolean = False
        main = DAQ()
        main.write_json({},file_name,boolean)


        
        for number in range(1, pairs_devices+1):
            data = {}

            with nidaqmx.Task() as output_task:
                output_task.ao_channels.add_ao_voltage_chan(analog_output)  # Replace with your channel name

                output_task.write(desired_voltage)

                with nidaqmx.Task() as input_task:
                    input_task.ai_channels.add_ai_voltage_chan(analog_input)  # Replace with your channel name

                    sample_rate = num_samples / desired_time  # Set the sample rate based on the desired time and number of samples
                    input_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

                    voltage_data = input_task.read(number_of_samples_per_channel=num_samples, timeout=float("1000"))

            current_data = [GAIN * voltage for voltage in voltage_data]

            time = np.linspace(0, (num_samples - 1) / sample_rate, num_samples)
            number_pair = f"Pair number: {number}"
            res = dict(zip(np.round(time, 1), current_data))
            data[number_pair] = res
            main.write_json(data,file_name,boolean=True)

            plt.plot(time, current_data)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (A)')
            plt.title(f'Current vs. Time pair number {pairs_devices}')
            plt.grid(True)
            plt.show()
        self.user_interface.ending()

        # Plot the current measurements over time
       
        

boolean = False
UI().start()
