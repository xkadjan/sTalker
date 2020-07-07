#!/usr/bin/python3
import time
import serial

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")


serial_port = serial.Serial(
 # set on: inverted logic, baud rate of 100000, 8 data bits, even parity bit, and 2 stop bits
    port="/dev/ttyTHS1",
    baudrate=100000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO,
)
# Wait a second to let the port initialize
time.sleep(1)

try:
    # Send a simple header

    print("start")
    for i in range(10):
        message = b'\x0f\x04$\xa0\xbc\x08\x08@\x00\x02\x10\x80\x00\x04 \x00\x01\x08@\x00\x02\x10\x80\x00$'
        serial_port.write(message)
        print("sent:", message)
        time.sleep(0.01)
#    serial_port.write("NVIDIA Jetson Nxxxxano Developer Kit\r\n".encode())
    print("end")


#    while True:
#        if serial_port.inWaiting() > 0:
#            data = serial_port.read()
#            print(data)
#            serial_port.write(data)
#            # if we get a carriage return, add a line feed too
#            # \r is a carriage return; \n is a line feed
#            # This is to help the tty program on the other end
#            # Windows is \r\n for carriage return, line feed
#            # Macintosh and Linux use \n
#            if data == "\r".encode():
#                # For Windows boxen on the other end
#                serial_port.write("\n".encode())


except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass