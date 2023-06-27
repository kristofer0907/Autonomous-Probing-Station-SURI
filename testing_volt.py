import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math
VOLTAGE_LEVEL = 1
analog_input_channel = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
analog_output_channel = "cDAQ1Mod1/ao0"
SAMPLE_AMOUNT = 10
FREQUENCY = 1000


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



set_analog_output(analog_output_channel,VOLTAGE_LEVEL,FREQUENCY,SAMPLE_AMOUNT)

voltage_reading,acquisition_time_voltage = read_voltage(analog_input_channel,SAMPLE_AMOUNT)