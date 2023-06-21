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

    def get_user_parameters(self,sample_amount,sample_rate,file_name):
        self.sample_amount = sample_amount
        self.sample_rate = sample_rate
        self.file_name = file_name

    def get_zeros(self,min,max,count=0 ):
        min = str(min)
        if min[count]:
            return self.get_zeros(min,max,count) 
        else:
            self.zeros = count
    

    

    def create_interval(self,start, end, step):
        interval_list = []
        num = start
        self.zeros = start.count(0)
        while round(num,self.zeros) <= end:
            interval_list.append(round(num,self.zeros))
            num += step
        return interval_list

    def setup(self,interval,steps,string):
        self.steps = steps        
        file_path =r"c:\Users\kdkristj\Desktop\GitHub\auto-prober-2023\data_files\\"
        voltage_min = min(interval)
        start_voltage = voltage_min
        self.start_voltage = start_voltage
        voltage_max = max(interval)
        self.start_voltage_max = voltage_max
        iterations = 2
        
        ############SETUP############
        actual_file = file_path+self.file_name
        self.actual_file = actual_file

        ############VOLTAGE############
        if type(string) == str:
            pass
       

         ############CURRENT############ 
        elif type(string) == int:
            pass   
        data = {}
        
        while start_voltage <=voltage_max:
            data[round(start_voltage,self.zeros)] = {}
            x = 1
            while x <= iterations:
                data[round(start_voltage,self.zeros)][x] = ""

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


    def storing(self,current_voltage,collected_data,iteration):
        '''Keep the data acquired in a dict'''        
        with open(self.actual_file,'r') as json_file:
            data = json.load(json_file)
        data[str(round(current_voltage,self.zeros))][str(iteration)] = collected_data
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
                #selecting data from which files
start_time = time.time()
analog_input_channel = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
analog_output_channel = "cDAQ1Mod1/ao0"
SAMPLE_AMOUNT = 10
SAMPLE_RATE = 1000
VOLTAGE_MIN = -0.05
VOLTAGE_MAX = 0.05
STEPS = 0.01
ITERATIVES = 2


############## CALLING MAIN ############## 


main = DAQ(analog_input_channel,analog_output_channel)
main.get_user_parameters(SAMPLE_AMOUNT,SAMPLE_RATE,file_name)
voltage_levels = main.create_interval(VOLTAGE_MIN,VOLTAGE_MAX,STEPS) # TODO: Make interval muteable for user
main.setup(voltage_levels,STEPS,str)
 ### How many times the user wants to execute each single voltage characteristic
 ## check holder

for voltage_level in voltage_levels:
    x = 1
    while x <= ITERATIVES:    
        main.set_analog_output(analog_output_channel,voltage_level,SAMPLE_AMOUNT)
        current_reading,current_time = main.read_current(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
        #voltage_reading,voltage_time = main.read_voltage(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
        main.storing(voltage_level,current_reading,x)
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


