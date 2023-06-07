import numpy as np
import nidaqmx

def read_voltage(channel_name,sample_amount):    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel_name)
        data = task.read(number_of_samples_per_channel= sample_amount)
        voltage = np.mean(data)
        return voltage







channel_name = "cDAQ1Mod2/ai0"  # Replace with the appropriate channel name for your setup
sample_amount = 20
voltage_reading = read_voltage(channel_name,sample_amount)
print(f"Average voltage reading: {voltage_reading} V")


