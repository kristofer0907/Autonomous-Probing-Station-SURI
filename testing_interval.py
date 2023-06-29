import nidaqmx

def validate_input(device_name, channel_name):
    try:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(f"{device_name}/{channel_name}")
            
        return True
    except nidaqmx.DaqError:
        return False


def validate_output(device_name, channel_name):
    try:
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(f"{device_name}/{channel_name}")
        return True
    except nidaqmx.DaqError:
        return False




# Example usage
device_name_input = "cDAQ1Mod2"
device_name_output = "cDAQ1Mod1"
analog_input_channel = "ai0"
analog_output_channel = "ao0"

is_input_valid = validate_input(device_name_input, analog_input_channel)
is_output_valid = validate_output(device_name_output, analog_output_channel)

if is_input_valid and is_output_valid:
    print("Input and output channel names are valid.")
else:
    print("Invalid channel name(s). Please check the names provided.")
