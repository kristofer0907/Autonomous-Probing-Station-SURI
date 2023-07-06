# import nidaqmx
# from nidaqmx.constants import AcquisitionType, VoltageUnits

# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan("cDAQ1Mod1/ao0")  # Replace with the appropriate channel name
#     task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=AcquisitionType.CONTINUOUS)

#     waveform = [0.0, 0.1,0, -0.1, 0.0]  # Replace with your desired waveform values
#     task.write(waveform, auto_start=True)
#     task.wait_until_done(timeout=100)
# import nidaqmx
# from nidaqmx.constants import AcquisitionType, VoltageUnits

# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan("cDAQ1Mod1/ao0")  # Replace with the appropriate channel name
#     task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=AcquisitionType.CONTINUOUS)

#     amplitude = 0.1  # Amplitude of the triangular waveform
#     frequency = 100.0  # Frequency of the triangular waveform
#     num_cycles = 1  # Number of cycles of the waveform
#     num_samples = int(task.timing.samp_clk_rate * num_cycles / frequency)

#     waveform = []
#     for i in range(num_samples):
#         t = i / task.timing.samp_clk_rate  # Time in seconds
#         value = amplitude * (2 * abs((t * frequency) % 1) - 1)
#         waveform.append(value)

#     task.write(waveform, auto_start=True)
#     task.wait_until_done(timeout=100)
# import nidaqmx
# import numpy as np
# from nidaqmx.constants import AcquisitionType, VoltageUnits

# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan("cDAQ1Mod1/ao0")  # Replace with the appropriate channel name
#     task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=AcquisitionType.CONTINUOUS)

#     amplitude = 0.1  # Amplitude of the triangular waveform (0.1V)
#     frequency = 100  # Frequency of the triangular waveform (1 Hz)
#     num_cycles = 5  # Number of cycles of the waveform
#     num_samples_per_cycle = 1000

#     waveform = []
#     time = np.linspace(0, num_cycles / frequency, num_samples_per_cycle * num_cycles)
#     voltage_steps = np.linspace(-amplitude, amplitude, int(2 * amplitude / 0.01) + 1)
#     waveform = np.interp((time * frequency) % 1, np.linspace(0, 1, len(voltage_steps)), voltage_steps)

#     task.write(waveform, auto_start=True)
#     task.wait_until_done(timeout=100)
1e-9
import nidaqmx

# Define voltage range and step size
voltage_min = -0.1
voltage_max = 0.1
voltage_step = 0.01

# Create a task for analog output
with nidaqmx.Task() as output_task:
    output_task.ao_channels.add_ao_voltage_chan("cDAQ1Mod1/ao0", min_val=voltage_min, max_val=voltage_max)

    # Create a task for analog input
    with nidaqmx.Task() as input_task:
        input_task.ai_channels.add_ai_voltage_chan("cDAQ1Mod2/ai0")

        # Set initial output voltage to 0V
        output_task.write(0)

        # Increase voltage to max
        for voltage in range(0, int(voltage_max * 100) + 1, int(voltage_step * 100)):
            voltage /= 100.0
            output_task.write(voltage)
            input_voltage = input_task.read()
            print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")

        # Decrease voltage to min
        for voltage in range(int(voltage_max * 100)-1, int(voltage_min * 100) - 1, -int(voltage_step * 100)):
            voltage /= 100.0
            output_task.write(voltage)
            input_voltage = input_task.read()
            print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")

        # Traverse back up to 0V
        for voltage in range(int(voltage_min * 100)+1, int(voltage_step+1), int(voltage_step * 100)):
            voltage /= 100.0
            output_task.write(voltage)
            input_voltage = input_task.read()
            print(f"Output Voltage: {voltage}V | Input Voltage: {input_voltage}V")
