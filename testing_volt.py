import nidaqmx

class NIcDAQ9174:
    def __init__(self, output_channel, input_channel, min_voltage=-1.0, max_voltage=1.0):
        self.output_channel = output_channel
        self.input_channel = input_channel
        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
        
        # Create tasks for analog output and input
        self.task_output = nidaqmx.Task()
        self.task_input = nidaqmx.Task()
        
        # Configure analog output channel
        self.task_output.ao_channels.add_ao_voltage_chan(self.output_channel, min_val=self.min_voltage, max_val=self.max_voltage)
        
        # Configure analog input channel
        self.task_input.ai_channels.add_ai_voltage_chan(self.input_channel)
    
    def set_voltage(self, voltage):
        self.task_output.write(voltage)
    
    def read_voltage(self):
        return self.task_input.read()

    def close(self):
        self.task_output.close()
        self.task_input.close()

# Example usage
cdaq = NIcDAQ9174("cDAQ1Mod1/ao0", "cDAQ1Mod2/ai0")

# Set voltage and read output voltage
cdaq.set_voltage(-1)
output_voltage = cdaq.read_voltage()
print("Output Voltage: {} V".format(output_voltage))

# Set a different voltage and read output voltage
cdaq.set_voltage(1)
output_voltage = cdaq.read_voltage()
print("Output Voltage: {} V".format(output_voltage))

# Cleanup
cdaq.close()

GAIN = 1e-9
junction_current = output_voltage*GAIN

