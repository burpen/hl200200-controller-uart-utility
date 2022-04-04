# Overview
This is a utility for UART communication with the Power Solutions "Motor PWM HL200200 v1.05" controller.

## Dependencies
* Python 3
* [pySerial](https://pyserial.readthedocs.io/)

## Setup
1. Open `config.ini`.
1. Update serial settings according to your environment.
1. Update UART address of your controller if necessary.

## Example usage
    python -i controller.py 						// Open the script in interactive mode
    readRegister(ReadCommand.SPEEDMOTOR1)			// Read the SPEEDMOTOR1 register
    writeRegister(WriteCommand.CURRENTLIMIT, 0xFF)	// Write 0xFF to the CURRENTLIMIT register
	readAllValues()									// Read all available registers and write the values to "data.txt"
	writeAllValues()								// Read values from "data.txt" and write them to the controller