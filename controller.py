#!/usr/bin/env python

from enum import Enum
import serial

# Address = UNIT_ADDRESS | 0x80
# By default the address is 0x00
address = bytearray.fromhex("80")

# Lookup class for read registers
class ReadRegister(bytearray):
    SPEEDMOTOR1 = bytearray.fromhex("00")
    CURRENTLIMIT = bytearray.fromhex("02")
    # TODO: the rest of the owl...

# Lookup class for write registers    
class WriteRegister(bytearray):
    SPEEDMOTOR1 = bytearray.fromhex("40")
    CURRENTLIMIT = bytearray.fromhex("42")
    # TODO: the rest of the owl...

# Read the specified register
def readRegister(readRegister):
    with serial.Serial() as ser:
        ser.baudrate = 19200
        ser.port = '/dev/ttyS0'
        ser.open()
        ser.write(address)
        ser.write(readRegister)
        # response should be 3 bytes
        response = ser.read(3)
        # TODO: check CRC
        # CRC should be ((Read command byte + 1th DATA byte + 2th DATA byte) & 0x7F)
        print(bytearray.hex(response))

# Write the payload to the specified register
def writeRegister(writeRegister, payload):
    if len(payload) != 2:
        raise Exception("Payload must be exactly 2 bytes")    
    # TODO: calculate the CRC and append to payload
    with serial.Serial() as ser:
        ser.baudrate = 19200
        ser.port = '/dev/ttyS0'
        ser.open()
        ser.write(address)
        ser.write(writeRegister)
        ser.write(payload)
        response = ser.read(1)
        # TODO: check CRC
        # CRC should be ((Write command byte + 1th DATA byte + 2th DATA byte) & 0x7F)
        print(bytearray.hex(response))

if __name__ == '__main__':
    #readRegister(ReadRegister.SPEEDMOTOR1)
    #writeRegister(WriteRegister.CURRENTLIMIT, bytearray([0,4]))