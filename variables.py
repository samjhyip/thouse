from collections import OrderedDict
appliances = OrderedDict()

#Basic Switch Settings
appliances["TESTsubject"] = "OFF"
appliances["doorBell"] = "OFF"
appliances["App3"] = "OFF"
appliances["App4"] = "OFF"

#integers To be set up as GPIO output
pins_to_use = [7,16,13,11]


#Input Settings
appliances_to_arm = ["doorbellSwitch", "Main Door"]
inputs_to_use = [19, 21]


#D'logging Settings
logsfolderpath = "/home/pi/automation_logs/"
turn_on_logging = True


#Pushbullet Settings
api_key = 'v1AKK5CDIVoP3iYjKDhVNHihZQjY4yYDEvujwirvOODWm'







"""
t.HOUSE by samjhyip

Necessary libraries to be installed:
Pushbullet
pytz
Python Screen



Functions available:
1) Basic relay switch operation
2) Listening to single button press in the background
3) Listening to constant button press and release in the background
4) Pushbullet notification API
5) Logging
6) TimeStamp Function

Future developments:
1) User preferred settings
2) PHP UI integration
3) Voice recognition and tasking
4) GUI
5) Scheduled tasking
6) Weather updates
7) Python NXT for motor control






So what I did was to make sure those modules were not loaded at boot-time - if this is the issue, then create /etc/modprobe.d/gpio-blacklist.conf and put in it:

CODE: SELECT ALL
blacklist spi_bcm2708
blacklist i2c_bcm2708
blacklist w1-gpio

You can always use the modprobe command to re-load those modules later if you have a project that uses SPI or I2C.
"""