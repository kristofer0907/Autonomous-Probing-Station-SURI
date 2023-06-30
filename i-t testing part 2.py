# import matplotlib.pyplot as plt
# import numpy as np
# import nidaqmx
# import time

# # Prompt the user to enter the desired measurement time
# desired_time = float(input("Enter the desired measurement time in seconds: "))

# # Create a task
# with nidaqmx.Task() as task:
#     # Add an analog input voltage channel
#     task.ai_channels.add_ai_voltage_chan("CDAQ1Mod2/ai0")  # Replace with your channel name
   
#     # Configure timing settings
#     sample_rate = 1000  # Set the desired sample rate in Hz
#     num_samples = int(sample_rate * desired_time)

#     task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

#     # Start the task
#     task.start()

#     # Read the voltage data
#     voltage_data = []

#     while len(voltage_data) < num_samples:
#         samples_to_read = min(num_samples - len(voltage_data), task.in_stream.avail_samp_per_chan)
#         voltage_data.extend(task.read(number_of_samples_per_channel=samples_to_read))

#     # Stop the task
#     task.stop()

# # Calculate the current from the voltage data
# current_data = [10 * voltage for voltage in voltage_data]

# # Generate the time axis for the plot
# time = np.linspace(0, desired_time, len(current_data))

# # Plot the current measurements over time
# plt.plot(time, current_data)
# plt.xlabel('Time (s)')
# plt.ylabel('Current (A)')
# plt.title('Current vs. Time')
# plt.grid(True)
# plt.show()import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx

# Prompt the user to enter the desired voltage level and measurement time
desired_voltage = float(input("Enter the desired voltage level in volts: "))
desired_time = float(input("Enter the desired measurement time in seconds: "))
num_samples = int(input("Enter the number of samples to acquire: "))

# Create a task for analog input
with nidaqmx.Task() as input_task:
    # Add an analog input voltage channel
    input_task.ai_channels.add_ai_voltage_chan("CDAQ1Mod2/ai0")  # Replace with your channel name

    # Configure timing settings
    sample_rate = num_samples / desired_time  # Set the sample rate based on the desired time and number of samples
    input_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

    # Read the voltage data
    voltage_data = input_task.read(number_of_samples_per_channel=num_samples,timeout=float("1000"))

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
