[README.md](https://github.com/user-attachments/files/21958693/README.md)
IoT Home Weather Station
This project is a prototype of a home weather station that uses an Internet of Things (IoT) approach to collect and display real-time environmental data. A Raspberry Pi with a Sense HAT acts as the sensor device, publishing temperature, humidity, and pressure data. A separate computer or device acts as a gateway, subscribing to and displaying this data.

Requirements
Hardware:

Raspberry Pi (model 4 recommended)

Raspberry Pi Sense HAT

A second computer (e.g., a laptop) to act as the gateway

Software & Libraries:

Python 3 installed on both devices

paho-mqtt Python library

sense-hat Python library (on the Raspberry Pi only)

Setup and Installation
Before running the project, you need to install the necessary libraries on your devices.

On the Raspberry Pi (for sensor.py):
Open a terminal and run the following commands to install the required libraries:

pip3 install paho-mqtt
sudo apt-get install sense-hat
pip3 install sense-hat

On your gateway computer (for gateway.py):
Open a terminal and install the MQTT library:

pip3 install paho-mqtt

How to Run the Project
Run the Gateway:
First, start the gateway script on your computer. This script will connect to the public MQTT broker and wait for messages.

python3 gateway.py

Run the Sensor:
Next, start the sensor script on your Raspberry Pi. This script will begin reading data from the Sense HAT and publishing it to the MQTT broker.

python3 sensor.py

You should now see the weather data appearing in the terminal of your gateway computer in real time.
