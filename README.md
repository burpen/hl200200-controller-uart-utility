# Overview
This is a utility for UART communication with "Motor PWM HL200200 v1.05" controller.

## Example usage
    readRegister(ReadCommand.SPEEDMOTOR1)
    writeRegister(WriteCommand.CURRENTLIMIT, 0xFF)