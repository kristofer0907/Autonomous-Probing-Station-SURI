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



# import matplotlib.pyplot as plt
# import numpy as np
# import nidaqmx

# # Prompt the user to enter the desired voltage level and measurement time
# desired_voltage = float(input("Enter the desired voltage level in volts: "))
# desired_time = float(input("Enter the desired measurement time in seconds: "))
# num_samples = int(input("Enter the number of samples to acquire: "))

# # Create a task for analog input
# with nidaqmx.Task() as input_task:
#     # Add an analog input voltage channel
#     input_task.ai_channels.add_ai_voltage_chan("CDAQ1Mod2/ai0")  # Replace with your channel name

#     # Configure timing settings
#     sample_rate = num_samples / desired_time  # Set the sample rate based on the desired time and number of samples
#     input_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

#     # Read the voltage data
#     voltage_data = input_task.read(number_of_samples_per_channel=num_samples,timeout=float("1000"))

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
# plt.show()
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx

GAIN = 1e-9
# Prompt the user to enter the desired voltage level and measurement time
desired_voltage = float(input("Enter the desired voltage level in volts: "))
desired_time = float(input("Enter the desired measurement time in seconds: "))
num_samples = int(input("Enter the number of samples to acquire: "))

# Create a task for analog output
with nidaqmx.Task() as output_task:
    # Add an analog output voltage channel
    output_task.ao_channels.add_ao_voltage_chan("CDAQ1Mod1/ao0")  # Replace with your channel name

    # Configure the desired voltage level
    output_task.write(desired_voltage)

    # Create a task for analog input
    with nidaqmx.Task() as input_task:
        # Add an analog input voltage channel
        input_task.ai_channels.add_ai_voltage_chan("CDAQ1Mod2/ai0")  # Replace with your channel name

        # Configure timing settings
        sample_rate = num_samples / desired_time  # Set the sample rate based on the desired time and number of samples
        input_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

        # Read the voltage data
        voltage_data = input_task.read(number_of_samples_per_channel=num_samples, timeout=float("1000"))

# Calculate the current from the voltage data
current_data = [GAIN * voltage for voltage in voltage_data]

# Generate the time axis for the plot
# Generate the time axis for the plot
time = np.linspace(0, (num_samples-1) / sample_rate, num_samples)


# Perform linear fit using numpy polyfit
fit_coeffs = np.polyfit(time, current_data, 1)  # Fit a line (degree 1 polynomial)
fit_line = np.polyval(fit_coeffs, time)  # Generate the fitted line values

# Plot the current measurements over time and the linear fit line
plt.plot(time, current_data, label='Data')
plt.plot(time, fit_line, label='Linear Fit')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Current vs. Time')
plt.legend()
plt.grid(True)
plt.show()
