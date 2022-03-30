# Overview
This is a utility for UART communication with the Power Solutions "Motor PWM HL200200 v1.05" controller.

## Dependencies
* Python 3
* [pySerial](https://pyserial.readthedocs.io/)

## Example usage
    readRegister(ReadCommand.SPEEDMOTOR1)
    writeRegister(WriteCommand.CURRENTLIMIT, 0xFF)