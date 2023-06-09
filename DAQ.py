import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math

def set_analog_output(analog_input_channel,voltage_level,rate,num_samples):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(analog_input_channel)
        task.timing.cfg_samp_clk_timing(rate=rate,samps_per_chan=num_samples)
        task.write(voltage_level)
        

def read_voltage(analog_input_channel,SAMPLE_AMOUNT):    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(analog_input_channel)
        start_time = time.perf_counter()
        data = task.read(number_of_samples_per_channel= SAMPLE_AMOUNT)
        end_time = time.perf_counter()
        elapsed_time= end_time-start_time
        average = np.mean(data)
       
        return data, elapsed_time
    
def read_current(analog_input_channel,SAMPLE_AMOUNT,period):    
    with nidaqmx.Task() as task:
       
        task.ai_channels.add_ai_current_chan(analog_input_channel)
        #task.ai_channels.add_ai_current_rms_chan(analog_input_channel)

        data = task.read(number_of_samples_per_channel= SAMPLE_AMOUNT)
        average = np.mean(data)

        return data
        

def plotter(I_data,V_data):
    plt.plot(V_data,I_data)
    plt.show()




# TODO: Change into rms values for better I-V reading
# TODO: Make the two data acquisition for voltage and current into a single function
start_time = time.time()
VOLTAGE_LEVEL = 0.0005
analog_input_channel = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
analog_output_channel = "cDAQ1Mod1/ao0"
SAMPLE_AMOUNT = 1200
FREQUENCY = 1000
set_analog_output(analog_output_channel,VOLTAGE_LEVEL,FREQUENCY,SAMPLE_AMOUNT)
time.sleep(1)
voltage_reading,acquisition_time_voltage = read_voltage(analog_input_channel,SAMPLE_AMOUNT)
period = (2*math.pi)/FREQUENCY

current_reading = read_current(analog_input_channel,SAMPLE_AMOUNT,period)
#print(f"Voltage reading: {voltage_reading} V")
print(f"Analog input acquisition time: {acquisition_time_voltage} seconds")
#print(f"Current reading: {current_reading} A")

print(len(voltage_reading))
print(len(current_reading))
print()
print(f"time it took to measure: {time.time()-start_time}")
#plotter(current_reading,voltage_reading)




