#!/usr/bin/env python

import serial

# Address = UNIT_ADDRESS | 0x80
# By default the address is 0x00
address = bytearray.fromhex("80")

# Lookup class for read register commands
class ReadCommand(bytearray):
    SPEEDMOTOR1 = bytearray.fromhex("00")
    CURRENTLIMIT = bytearray.fromhex("02")
    REGENLIMIT = bytearray.fromhex("03")
    ACCELLIMIT = bytearray.fromhex("04")
    DECELLIMIT = bytearray.fromhex("05")
    TURNOFFLOW = bytearray.fromhex("06")
    TURNONLOW = bytearray.fromhex("07")
    TURNONHIGH = bytearray.fromhex("08")
    TURNOFFHIGH = bytearray.fromhex("09")
    HEATSINKTEMPERATURE = bytearray.fromhex("0A")
    MAINBOARDTEMPERATURE = bytearray.fromhex("0B")
    UNUSED1 = bytearray.fromhex("0F")
    SUPPLYVOLTAGE = bytearray.fromhex("10")
    SPEEDADCINPUT = bytearray.fromhex("11")
    LOADCURRENT1 = bytearray.fromhex("12")
    INPUTFREQUENCYPERIODREGISTER = bytearray.fromhex("14")
    INPUTPULSEWIDTH = bytearray.fromhex("15")
    UNUSED2 = bytearray.fromhex("19")
    IRCOMPENSATIONGAIN = bytearray.fromhex("20")
    TOPSPEED = bytearray.fromhex("21")
    POTENTIOMETERMIN = bytearray.fromhex("22")
    POTENTIOMETERMAX = bytearray.fromhex("23")
    UNUSED3 = bytearray.fromhex("24")
    STATUSREGISTER = bytearray.fromhex("30")
    LOCKLEVEL2VARIABLES = bytearray.fromhex("31")
    SAVEBYTES1 = bytearray.fromhex("32")
    SAVEBYTES2 = bytearray.fromhex("33")
    CONFIGURATIONBITS1 = bytearray.fromhex("34")
    CONFIGURATIONBITS2 = bytearray.fromhex("35")
    SOFTWAREVERSION = bytearray.fromhex("3E")
    HARDWAREVERSION = bytearray.fromhex("3F")

# Lookup class for write registers    
class WriteCommand(bytearray):
    SPEEDMOTOR1 = bytearray.fromhex("40")
    CURRENTLIMIT = bytearray.fromhex("42")
    REGENLIMIT = bytearray.fromhex("43")
    ACCELLIMIT = bytearray.fromhex("44")
    DECELLIMIT = bytearray.fromhex("45")
    TURNOFFLOW = bytearray.fromhex("46")
    TURNONLOW = bytearray.fromhex("47")
    TURNONHIGH = bytearray.fromhex("48")
    TURNOFFHIGH = bytearray.fromhex("49")
    IRCOMPENSATIONGAIN = bytearray.fromhex("60")
    TOPSPEED = bytearray.fromhex("61")
    POTENTIOMETERMIN = bytearray.fromhex("62")
    POTENTIOMETERMAX = bytearray.fromhex("63")
    LOCKLEVEL2VARIABLES = bytearray.fromhex("71")
    SAVEBYTES1 = bytearray.fromhex("72")
    SAVEBYTES2 = bytearray.fromhex("73")
    CONFIGURATIONBITS1 = bytearray.fromhex("74")
    CONFIGURATIONBITS2 = bytearray.fromhex("75")
    UARTADDRESS = bytearray.fromhex("7C")
    CURRENTMEASUREMENTCALIBRATION = bytearray.fromhex("7D")

# Read the specified register
def readRegister(readCommand):
    with serial.Serial() as ser:
        ser.baudrate = 19200
        ser.port = '/dev/ttyS0'
        ser.open()
        ser.write(address)
        ser.write(readCommand)
        # response should be 3 bytes
        response = ser.read(3)
        # TODO: check CRC
        # CRC should be ((Read command byte + 1th DATA byte + 2th DATA byte) & 0x7F)
        print(bytearray.hex(response))

# Write the payload to the specified register
def writeRegister(writeCommand, payload):
    if len(payload) != 2:
        raise Exception("Payload must be exactly 2 bytes")    
    # TODO: calculate the CRC and append to payload
    with serial.Serial() as ser:
        ser.baudrate = 19200
        ser.port = '/dev/ttyS0'
        ser.open()
        ser.write(address)
        ser.write(writeCommand)
        ser.write(payload)
        response = ser.read(1)
        # TODO: check CRC
        # CRC should be ((Write command byte + 1th DATA byte + 2th DATA byte) & 0x7F)
        print(bytearray.hex(response))

if __name__ == '__main__':
    readRegister(ReadCommand.SPEEDMOTOR1)
    #writeRegister(writeCommand.CURRENTLIMIT, bytearray([0,4]))