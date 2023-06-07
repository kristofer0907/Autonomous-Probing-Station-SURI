import numpy as np
import nidaqmx
import time
def read_voltage(channel_name,sample_amount):    
    with nidaqmx.Task() as task:
        start_time = time.time()
        #task.ai_channels.add_ai_voltage_chan(channel_name)
        task.ai_channels.add_ai_current_chan(channel_name)
        data = task.read(number_of_samples_per_channel= sample_amount)
        voltage = np.mean(data)
        end_time = time.time()-start_time
        print(end_time)
        return voltage
        
#TODO Figure out why python is much quicker at collecting data than DAQ software is






channel_name = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
sample_amount = 1200
voltage_reading = read_voltage(channel_name,sample_amount)
print(f"Average voltage reading: {voltage_reading} V")


