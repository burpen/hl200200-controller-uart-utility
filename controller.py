#!/usr/bin/env python

from enum import Enum
import serial

# Address = UNIT_ADDRESS | 0x80
# By default the address is 0x00
address =           0x00 | 0x80

minPayloadValue =   0x0000
maxPayloadValue =   0x0FFF

serialBaudRate =    19200
serialPort =        '/dev/ttyS0'

# Lookup class for read register commands
class ReadCommand(Enum):
    SPEEDMOTOR1 =                   0x00
    CURRENTLIMIT =                  0x02
    REGENLIMIT =                    0x03
    ACCELLIMIT =                    0x04
    DECELLIMIT =                    0x05
    TURNOFFLOW =                    0x06
    TURNONLOW =                     0x07
    TURNONHIGH =                    0x08
    TURNOFFHIGH =                   0x09
    HEATSINKTEMPERATURE =           0x0A
    MAINBOARDTEMPERATURE =          0x0B
    UNUSED1 =                       0x0F
    SUPPLYVOLTAGE =                 0x10
    SPEEDADCINPUT =                 0x11
    LOADCURRENT1 =                  0x12
    INPUTFREQUENCYPERIODREGISTER =  0x14
    INPUTPULSEWIDTH =               0x15
    UNUSED2 =                       0x19
    IRCOMPENSATIONGAIN =            0x20
    TOPSPEED =                      0x21
    POTENTIOMETERMIN =              0x22
    POTENTIOMETERMAX =              0x23
    UNUSED3 =                       0x24
    STATUSREGISTER =                0x30
    LOCKLEVEL2VARIABLES =           0x31
    SAVEBYTES1 =                    0x32
    SAVEBYTES2 =                    0x33
    CONFIGURATIONBITS1 =            0x34
    CONFIGURATIONBITS2 =            0x35
    SOFTWAREVERSION =               0x3E
    HARDWAREVERSION =               0x3F

# Lookup class for write registers    
class WriteCommand(Enum):
    SPEEDMOTOR1 =                   0x40
    CURRENTLIMIT =                  0x42
    REGENLIMIT =                    0x43
    ACCELLIMIT =                    0x44
    DECELLIMIT =                    0x45
    TURNOFFLOW =                    0x46
    TURNONLOW =                     0x47
    TURNONHIGH =                    0x48
    TURNOFFHIGH =                   0x49
    IRCOMPENSATIONGAIN =            0x60
    TOPSPEED =                      0x61
    POTENTIOMETERMIN =              0x62
    POTENTIOMETERMAX =              0x63
    LOCKLEVEL2VARIABLES =           0x71
    SAVEBYTES1 =                    0x72
    SAVEBYTES2 =                    0x73
    CONFIGURATIONBITS1 =            0x74
    CONFIGURATIONBITS2 =            0x75
    UARTADDRESS =                   0x7C
    CURRENTMEASUREMENTCALIBRATION = 0x7D

# Read the specified register
def readRegister(readCommand):
    with serial.Serial() as ser:
        ser.baudrate = serialBaudRate
        ser.port = serialPort
        ser.open()
        ser.write(address)
        ser.write(readCommand.value)
        # Response should be 3 bytes
        response = ser.read(3)
        # Check CRC
        # CRC should be (readCommand + first data byte + second data byte) & 0x7F
        crc = response[2]
        expectedCrc = (readCommand.value + response[0] + response[1]) & 0x7F
        if crc != expectedCrc:
            raise Exception("CRC failed. Expected {} but got {}".format(hex(expectedCrc), hex(crc)))
            return
        # Data = first byte << 7 | second byte & 0x7F
        data = response[0] << 7 | response[1] & 0x7F
        print("Read OK: {} ({}) = {}".format(readCommand.name, hex(readCommand.value), hex(data)))
        return data

# Write the payload to the specified register.
def writeRegister(writeCommand, payload):
    # Check that payload is within the min and max bounds
    if payload < minPayloadValue or payload > maxPayloadValue:
        raise Exception("Payload must be between {} and {} (inclusive)".format(hex(minPayloadValue), hex(maxPayloadValue)))
        return
    # Format the data bytes
    data0 = (payload >> 7) & 0x7F
    data1 = payload & 0x7F
    # TODO: calculate the CRC and append to payload
    with serial.Serial() as ser:
        ser.baudrate = serialBaudRate
        ser.port = serialPort
        ser.open()
        ser.write(address)
        ser.write(writeCommand.value)
        ser.write(data0)
        ser.write(data1)
        # Response should be 1 byte
        response = ser.read(1)
        # Check CRC
        # CRC should be (writeCommand + data0 + data1) & 0x7F
        expectedCrc = (writeCommand.value + data0 + data1) & 0x7F
        if (response != expectedCrc):
            raise Exception("CRC failed. Expected {} but got {}".format(hex(expectedCrc), hex(response)))
            return
    print("Write OK: {} ({}) set to {}".format(writeCommand.name, hex(writeCommand.value), hex(value)))
    return

if __name__ == '__main__':
    #readRegister(ReadCommand.SPEEDMOTOR1)
    writeRegister(WriteCommand.CURRENTLIMIT, 0xFF)