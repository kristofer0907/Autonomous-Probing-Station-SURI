import serial
COMPORT = "COM4"
ser = serial.Serial(COMPORT,9600,timeout=1)

def retrieveData():
    ser.write(b"1")
    data = ser.readline().decode("ascii")
    return data

while True:
    uInput = input("Retrieve data: ")
    if uInput == "1":
        print(retrieveData())
    else:
        ser.write(b"0")
