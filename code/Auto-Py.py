# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import serial
import time

# Configure the serial port
ser = serial.Serial('COM5', 9600)  # Replace 'COM1' with the appropriate port and baud rate

def send_command(command):
    ser.write(command.encode())
    time.sleep(0.1)

try:
    # Open the serial connection
    ser.open()
    time.sleep(2)  # Wait for the connection to establish

    # Send commands to control the stepper motor
    send_command("S1")  # Set direction 1
    for _ in range(8000):
        send_command("P")  # Step pulse
        time.sleep(0.001)

    send_command("S0")  # Set direction 0
    for _ in range(1000):
        send_command("P")  # Step pulse
        time.sleep(0.001)

    send_command("S0")  # Set direction 0
    for _ in range(1000):
        send_command("P")  # Step pulse
        time.sleep(0.001)

except serial.SerialException as e:
    print("Failed to communicate with the serial port:", e)
finally:
    # Close the serial connection
    ser.close()
