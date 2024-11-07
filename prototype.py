import network
import time
from math import sin
from umqtt.simple import MQTTClient
import urandom
from machine import Pin,I2C,ADC
import utime
import sgp30
from dht11 import DHT11, InvalidChecksum

# Fill in your WiFi network name (ssid) and password here:
wifi_ssid = "PCWAEL"
wifi_password = "12345678"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = "bay4v"  # Your Adafruit IO username
# put yours mqtt_password = ""  # Adafruit IO Key
mqtt_publish_topic = "bay4v/feeds/airfit"  # The MQTT topic for your Adafruit IO Feed

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "somethingreallyrandomandunique123airfit"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

counter = 0
try:
    while True:
        pin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        Temper=sensor.temperature
        humidi== sensor.humidity
        i2c_sgp30=I2C(1,sda=Pin(14),scl=Pin(15),freq=100000)
        handle_i2c=sgp30.SGP30(i2c_sgp30)
        co2,VOC=handle_i2c.indoor_air_quality
        Noise=ADC(28).read_u16()
        
        
        # Publish the data to the topic!
        msg=str(Temper)+" "+str(humidi)+" "+str(co2)+" "+str(VOC)+" " +str(Noise)+"  "
        print("Published" ,msg)
        mqtt_client.publish(mqtt_publish_topic,str(msg) )
        
        # Delay a bit to avoid hitting the rate limit
        time.sleep(9)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()
