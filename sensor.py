# This script runs on the Raspberry Pi with the Sense HAT.
# It reads sensor data and publishes it to an MQTT broker.

import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import json
import time

# --- Configuration ---
MQTT_BROKER_HOST = "broker.hivemq.com"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/my_home_weather"
CLIENT_ID = "RaspberryPi-Sensor-Client"

def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

def run_sensor_client():
    """Initializes and runs the sensor client."""
    # Create a SenseHat object
    sense = SenseHat()

    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect  # Assign the connect callback function

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return

    # The loop_start() method starts a background thread that handles
    # network traffic and calls the on_connect and on_message callbacks.
    client.loop_start()

    print(f"Publishing data to topic: {MQTT_TOPIC}")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # Read sensor data from the Sense HAT
            temperature = round(sense.get_temperature(), 2)
            humidity = round(sense.get_humidity(), 2)
            pressure = round(sense.get_pressure(), 2)

            # Create a dictionary to hold the sensor data
            payload = {
                "temperature_c": temperature,
                "humidity_percent": humidity,
                "pressure_mb": pressure,
                "timestamp": int(time.time())
            }

            # Convert the dictionary to a JSON string
            json_payload = json.dumps(payload)

            # Publish the JSON string to the topic
            result = client.publish(MQTT_TOPIC, json_payload)

            # Check the publish result and print a message
            status = result[0]
            if status == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: {json_payload}")
            else:
                print(f"Failed to publish message. Status: {status}")

            # Wait for 5 seconds before the next reading
            time.sleep(5)

    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop() # Stop the background thread
        client.disconnect() # Disconnect from the broker

if __name__ == '__main__':
    run_sensor_client()