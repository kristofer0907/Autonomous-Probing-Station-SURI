import serial
import time

COMPORT = "COM5"
arduino = serial.Serial(port = COMPORT, timeout=0)
time.sleep(2)

while True:

    print ("Enter numbers broski")

    var = str(input())
    print ("You Entered :", var)

    if(var == "1"):
        arduino.write(str.encode("1"))
        
        time.sleep(1)

    elif(var == "2"):
        arduino.write(str.encode("2"))
        time.sleep(1)
    elif(var == "3"):
        arduino.write(str.encode("3"))
        time.sleep(1)
    elif(var == "S"):
        arduino.write(str.encode("S"))
        time.sleep(1)
    while arduino.in_waiting:
        data = arduino.readline().decode().strip()
        if data:
            print("Arduino says:", data)

    arduino.flushInput()