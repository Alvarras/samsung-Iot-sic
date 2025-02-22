from machine import Pin
import ujson
import network
import utime as time
import dht
import urequests as requests

DEVICE_ID = "esp32_sic"
WIFI_SSID = "Poco X3"
WIFI_PASSWORD = ""
TOKEN = "BBUS-BNFTtR8psg2tsa4BfFRUXm1nOqB73f"

DHT1_PIN = Pin(15)
DHT2_PIN = Pin(17)
pir = Pin(34, Pin.IN)

dht_sensor1 = dht.DHT11(DHT1_PIN)
dht_sensor2 = dht.DHT11(DHT2_PIN)
pir_value = pir.value()
telemetry_data_old = ""

def create_json_data(temperature1, humidity1, temperature2, humidity2, pir_value):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "temp1": temperature1,
        "humidity1": humidity1,
        "temp2": temperature2,
        "humidity2": humidity2,
        "pir" : pir_value,
        "type": "sensor"
    })
    return data

def send_data(temperature1, humidity1, temperature2, humidity2, pir_value):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp1": temperature1,
        "humidity1": humidity1,
        "temp2": temperature2,
        "humidity2": humidity2,
        "pir" : pir_value
    }
    response = requests.post(url, json=data, headers=headers)
    print("Response:", response.text)

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting")
    time.sleep(0.1)
print("WiFi Connected!")
print(wifi_client.ifconfig())

while True:
    try:
        dht_sensor1.measure()
        dht_sensor2.measure()
    except:
        pass

    time.sleep(0.5)

    telemetry_data_new = create_json_data(dht_sensor1.temperature(), dht_sensor1.humidity(), dht_sensor2.temperature(), dht_sensor2.humidity(), pir_value)

    if telemetry_data_new != telemetry_data_old:
        telemetry_data_old = telemetry_data_new
        
        # Call the send_data function to send data to Ubidots
        send_data(dht_sensor1.temperature(), dht_sensor1.humidity(), dht_sensor2.temperature(), dht_sensor2.humidity(), pir_value)

time.sleep(0.3)