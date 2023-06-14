import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math

def set_analog_output(analog_input_channel,voltage_level,num_samples):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(analog_input_channel)
        #task.timing.cfg_samp_clk_timing(rate=rate,samps_per_chan=num_samples)
        task.write(voltage_level)

def read_voltage(channel_name,sample_amount,sample_rate):    
    with nidaqmx.Task() as task:

        #task.wait_until_done(timeout=1000)
        task.ai_channels.add_ai_voltage_chan(channel_name)
        task.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan=sample_amount)
        task.start()
        start_time= time.time()
        data = task.read(number_of_samples_per_channel= sample_amount,timeout=float("1000"))
        elapsed_time = time.time()-start_time
        time_array = np.linspace(0, elapsed_time, sample_amount)

        return data,time_array



def read_current(analog_input_channel,sample_amount,sample_rate):    
    with nidaqmx.Task() as task:
        #task.wait_until_done(timeout=1000)
        task.wait_until_done = float(sample_amount/sample_rate+1)

        task.ai_channels.add_ai_current_chan(analog_input_channel)
        task.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan=sample_amount)
        task.start()
        start_time= time.time()
        data = task.read(number_of_samples_per_channel= SAMPLE_AMOUNT,timeout=float("1000"))        
        elapsed_time = time.time()-start_time
        time_array = np.linspace(0, elapsed_time, sample_amount)

        return data,time_array
        #task.ai_channels.add_ai_current_rms_chan(analog_input_channel)

    
        

def plotter(x,y):
    plt.plot(x,y)
    plt.show()




# channel_name = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
# sample_amount = 1200
# voltage_reading = read_voltage(channel_name,sample_amount)
# print(f"Average voltage reading: {voltage_reading} V")

start_time = time.time()
VOLTAGE_LEVEL = 0.005
analog_input_channel = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
analog_output_channel = "cDAQ1Mod1/ao0"
SAMPLE_AMOUNT = 10
SAMPLE_RATE = 1000
set_analog_output(analog_output_channel,VOLTAGE_LEVEL,SAMPLE_AMOUNT)
#time.sleep(1)
voltage_reading,voltage_time = read_voltage(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)

current_reading,current_time = read_current(analog_input_channel,SAMPLE_AMOUNT,SAMPLE_RATE)
#print(f"Voltage reading: {voltage_reading} V")
#print(f"Analog input acquisition time: {acquisition_time_voltage} seconds")
#print(f"Current reading: {current_reading} A")


print(f"time of entire process: {time.time()-start_time}") # time the program takes to start
plotter(current_reading,voltage_reading) #plot voltage vs. current
#plotter(voltage_reading,voltage_time) #plot the time vs. current
#plotter(current_reading,current_time) #plot the time vs. voltage

