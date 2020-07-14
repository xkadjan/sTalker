#!/usr/bin/python3
"""
Created on Sat Jul  4 22:38:33 2020
This script solve simulation of transmission trough SBUS protocol
Logic Async Serial analyzer was set on: inverted logic, baud rate of 100000, 8 data bits, even parity bit, and 2 stop bits
inspirated by: https://github.com/1arthur1/PiSBUS
@author: xkadj
"""
import os,sys
import time
import serial
import logging

sys.path.append(os.path.join(sys.path[0]))
print(sys.path[0])

def set_logging():
    logfile = os.path.join('.', "serial_stream.log")
    logcfg = {
        'format'  : '%(asctime)s %(levelname)s: %(message)s',
        'level'   : logging.DEBUG,
        'filename': logfile}
    logging.basicConfig(**logcfg)

def load_stream():
    with open(os.path.join('.', 'record_binary.log'), "rb") as f:
        stream = f.read()
        return [b'\x0f' + x for x in stream.split(b'\x0f')][1:]

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=100000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO,
)

time.sleep(1) # Wait a second to let the port initialize
set_logging()
messages_list = load_stream()

try:
    # Send a simple header
    print("start")
    for message in messages_list:
        serial_port.write(message)
        print("sent:", message)
        logging.info("sent msg: " + str(message))
        time.sleep(0.0147)
    print("end")

except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass