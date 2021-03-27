import serial.tools.list_ports
from serial import Serial

# ports = serial.tools.list_ports.comports()
#
# for port, desc, hwid in sorted(ports):
#     print("{}: {} [{}]".format(port, desc, hwid))

ser = Serial("COM4", 9600, timeout=0.1)
ser.reset_input_buffer()

while True:
    if ser.inWaiting() > 1:
        waiting = ser.inWaiting()
        print(ser.read(waiting).decode())
# for i in range(5):
#     print("Ping")
#     ser.write(b"BOOP "+str.encode(str(i)))
#     input_data = ser.readline()
#     print(input_data.decode())
#     time.sleep(0.1)
# ser.close()
# print("Done")
