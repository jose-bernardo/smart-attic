# Description
Smart Attic is a system that leverages the potential of Internet-of-Things (IoT) technologies 
to address both the security and the safety issues that traditional attics pose. 
The system integrates a network of intelligent sensors to gather data about the attic environment 
and potential security breaches. This data is transmitted securely through secure 
communication protocols to a central hub (Raspberry Pi), where it is analyzed. Then, the system 
uses actuators that, based on the analysis done by the central hub, takes automated actions 
to ensure a swift and efficient response to security breaches or environmental threats.

# Requirements

## Hardware
Arduino configured with 4 LEDs, a DHT11 sensors, and a photoresistor sensor as the in the image below
Raspberry Pi
Keyboard (to connect to the Raspberry Pi)
USB video camera (to connect to the Raspberry Pi)

## Software
Python3
Arduino IDE

![Arduino Configuration](arduino_configuration.png)

# Web application
## Installation
```
cd webServer

pip3 install -r requirements.txt
```

## Run
```
cd webServer

# set database configurations
export DB_HOST = "your-database-host"
export DB_USERNAME = "your-db-username"
export DB_PASSWORD = "your-db-password"
export DB_NAME = "your-database-name"

# set admin email address and password to notify users
export ADMIN_MAIL_ADDRESS="admin-email-address"
export ADMIN_MAIL_PASSWORD="admin-email-password"

# set Raspberry Pi address
export PI_ADDRESS="pi-address"

# set email address corresponding to user1 for testing
export MAIL_ADDRESS="recipient-email-address"

# create directory to store footage
mkdir media

python3 webServer.py
```

# Arduino modules

Install Arduino IDE, connect your Arduino to your computer and upload the `sensors.ino` in [arduino-modules/sensors](arduino-modules/sensors) to the arduino.

# Raspberry Pi modules

## Installation

```
cd raspberry-modules

pip3 install -r requirements.txt
```

## Run

```
# set server host
export SERVER_URL="your-server-url"

# set serial port where arduino is connected (e.g. /dev/ttyACM0)
export SERIAL_PORT="connected-port"

# !!! You need to run the following three scripts
# for receiving serial data from arduino
python3 serial_reader.py

# for sending configuration data to arduino
python3 serial_sender.py

# to simulate security door
python3 keypad_reader.py
```
