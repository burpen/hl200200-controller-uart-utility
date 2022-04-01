#!/usr/bin/env python

from enum import Enum
import serial
import configparser

# Based on controller documentation, these are the hard min/max bounds for data
minPayloadValue =   0x0000
maxPayloadValue =   0x0FFF

# Name of data file for batch read/write operations
dataFileName = "data.txt"

# Open config file
config = configparser.ConfigParser()
config.read('config.ini')

# Read serial settings from config file
serialBaudRate =    int(config['Serial']['BaudRate'])
serialPort =        config['Serial']['Port']
serialTimeout =     int(config['Serial']['Timeout'])

# Read UART address from config file
address =           int(config['UART']['Address'], 16)

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

# Lookup class for write register commands    
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
    # Check that we have a valid read command
    if readCommand.value not in ReadCommand._value2member_map_:
        raise Exception("ReadCommand {} is not recognized".format(hex(readCommand.value)))
        return
    with serial.Serial() as ser:
        if __debug__:
            print("Connecting to {} at {} baud, {} second timeout...".format(serialPort, serialBaudRate, serialTimeout))
        ser.baudrate = serialBaudRate
        ser.port = serialPort
        ser.timeout = serialTimeout
        ser.open()
        if __debug__:
            print("Writing bytes {} {}...".format(hex(address), hex(readCommand.value)))
        # write() accepts bytes or bytearray type, so convert ints to bytes
        ser.write(address.to_bytes(1, byteorder='big'))
        ser.write(readCommand.value.to_bytes(1, byteorder='big'))
        # Response should be 3 bytes
        expectedResponseLength = 3
        response = ser.read(expectedResponseLength)
        if __debug__:
            print("Received {} bytes in response: {}".format(len(response), response))
        if (len(response) != expectedResponseLength):
            raise Exception("Response was {} bytes. Expected {} bytes.".format(len(response), expectedResponseLength))
            ser.close()
            return
        # Check CRC
        # CRC should be (readCommand + first data byte + second data byte) & 0x7F
        crc = response[2]
        expectedCrc = (readCommand.value + response[0] + response[1]) & 0x7F
        if crc != expectedCrc:
            raise Exception("CRC failed. Expected {} but got {}".format(hex(expectedCrc), hex(crc)))
            ser.close()
            return
        # Data = first byte << 7 | second byte & 0x7F
        data = response[0] << 7 | response[1] & 0x7F
        print("Read OK: {} ({}) = {}".format(readCommand.name, hex(readCommand.value), hex(data)))
        ser.close()
        return data

# Write the payload to the specified register.
def writeRegister(writeCommand, payload):
    # Check that we have a valid write command
    if writeCommand.value not in WriteCommand._value2member_map_:
        raise Exception("WriteCommand {} is not recognized".format(hex(writeCommand.value)))
        return
    # Check that payload is within the min and max bounds
    if payload < minPayloadValue or payload > maxPayloadValue:
        raise Exception("Payload must be between {} and {} (inclusive)".format(hex(minPayloadValue), hex(maxPayloadValue)))
        return
    # Format the data bytes
    data0 = (payload >> 7) & 0x7F
    data1 = payload & 0x7F
    # CRC should be (writeCommand + data0 + data1) & 0x7F
    expectedCrc = (writeCommand.value + data0 + data1) & 0x7F
    # TODO: calculate the CRC and append to payload
    with serial.Serial() as ser:
        if __debug__:
            print("Connecting to {} at {} baud, {} second timeout...".format(serialPort, serialBaudRate, serialTimeout))
        ser.baudrate = serialBaudRate
        ser.port = serialPort
        ser.timeout = serialTimeout
        ser.open()
        if __debug__:
            print("Writing bytes {} {} {} {} {}...".format(hex(address), hex(writeCommand.value), hex(data0), hex(data1), hex(expectedCrc)))
        # write() accepts bytes or bytearray type, so convert ints to bytes
        ser.write(address.to_bytes(1, byteorder='big'))
        ser.write(writeCommand.value.to_bytes(1, byteorder='big'))
        ser.write(data0.to_bytes(1, byteorder='big'))
        ser.write(data1.to_bytes(1, byteorder='big'))
        ser.write(expectedCrc.to_bytes(1, byteorder='big'))
        # Response should be 1 byte
        expectedResponseLength = 1
        response = ser.read(expectedResponseLength)
        if __debug__:
            print("Received {} bytes in response: {}".format(len(response), response))
        if (len(response) != expectedResponseLength):
            raise Exception("Response was {} bytes. Expected {} bytes.".format(len(response), expectedResponseLength))
            ser.close()
            return
        # Check CRC
        if (response != expectedCrc):
            raise Exception("CRC failed. Expected {} but got {}".format(hex(expectedCrc), response))
            ser.close()
            return
    print("Write OK: {} ({}) set to {}".format(writeCommand.name, hex(writeCommand.value), hex(value)))
    ser.close()
    return

# Read all registers and store results in an output file.
def readAllValues():
    with open(dataFileName,"w") as dataFile:
        for register in ReadCommand:
            print("Reading {}...".format(register))
            try:
                result = readRegister(register)
                print("Read {} OK".format(register))
                dataFile.write("{}:{}\n".format(register.name, result))
            except Exception as e:
                print("Failed to read {}. Caught {}".format(register, e))
                continue

def writeAllValues():
    with open(dataFileName,"r") as dataFile:
        lines = dataFile.readlines()
        for line in lines:
            try:
                lineKeyValuePair = line.split(":")
                register = WriteCommand[lineKeyValuePair[0]]
                value = int(lineKeyValuePair[1])
                print("Writing {}={}...".format(register, hex(value)))
                try:
                    writeRegister(register, value)
                    print("Write {}={} OK".format(register, hex(value)))
                except Exception as e:
                    print("Failed to write {}={}. Caught {}".format(register, hex(value), e))
                    continue
            except KeyError:
                # Ignore this line since the register is not writeable
                if __debug__:
                    print("Ignoring {} since it is not writeable.".format(lineKeyValuePair[0]))
                continue
            except Exception as e:
                print("Failed to parse '{}'. Caught {}".format(line, e))
                continue