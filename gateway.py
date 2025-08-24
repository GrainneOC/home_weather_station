# This script runs on laptop ("gateway").
# It subscribes to the MQTT topic and receives sensor data from the Raspberry Pi.

import paho.mqtt.client as mqtt
import json

# --- Configuration ---
# Same configuration as the sensor.py script
MQTT_BROKER_HOST = "broker.hivemq.com"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/my_home_weather"
CLIENT_ID = "Gateway-Receiver-Client"

def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
        # Subscribe to the topic when connected
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback function for when a message is received on the subscribed topic."""
    print(f"Received message on topic: {msg.topic}")

    try:
        # Decode the message payload and parse the JSON string
        payload = json.loads(msg.payload.decode('utf-8'))

        # Extract the sensor data
        temperature = payload.get("temperature_c")
        humidity = payload.get("humidity_percent")
        pressure = payload.get("pressure_mb")

        print("--- Sensor Data ---")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} millibar")
        print("-------------------")

    except json.JSONDecodeError:
        print("Error: Received message is not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def run_gateway_client():
    """Initializes and runs the gateway client."""
    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect  # Assign the connect callback function
    client.on_message = on_message  # Assign the message callback function

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return

    # This call blocks the program and allows the client to handle
    # network traffic and callbacks.
    client.loop_forever()

if __name__ == '__main__':
    run_gateway_client()