from machine import Pin
import network
import urequests
import utime as time
import ujson
import dht

# Koneksi ke WiFi, SSID & Password menyesuaikan
SSID = "BOHAY KOST"
PASSWORD = "05052021"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
print("Menghubungkan ke Wifi ", end="")
while not wifi.isconnected():
    print(".", end="")
    time.sleep(1)
print("Terhubung ke WiFi!")

# Data Ubidots
DEVICE_ID = "esp32_sic"
TOKEN = "BBUS-BNFTtR8psg2tsa4BfFRUXm1nOqB73f"
URL_UBIDOTS = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
HEADERS_UBIDOTS = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}

# IP Server Flask
flask_url = "http://192.168.1.13:5000/store"
header_flask = {"Content-Type": "application/json"}

# Data Sensor
DHT1_PIN = Pin(15)
DHT2_PIN = Pin(17)
pir = Pin(34, Pin.IN)

dht_sensor1 = dht.DHT11(DHT1_PIN)
dht_sensor2 = dht.DHT11(DHT2_PIN)
pir_value = pir.value()
telemetry_data_old = ""

def create_json_data(temperature1, humidity1, temperature2, humidity2, pir_value):
    data = ujson.dumps({
        "temp1": temperature1,
        "humidity1": humidity1,
        "temp2": temperature2,
        "humidity2": humidity2,
        "pir" : pir_value,
    })
    return data

def send_data(temperature1, humidity1, temperature2, humidity2, pir_value):
    data = {
        "temp1": temperature1,
        "humidity1": humidity1,
        "temp2": temperature2,
        "humidity2": humidity2,
        "pir" : pir_value
    }
    response_flask = urequests.post(flask_url, json=data, headers=header_flask)
    print("Response Flask :", response_flask.text)
    response_ubidots = urequests.post(URL_UBIDOTS, json=data, headers=HEADERS_UBIDOTS)
    print("Response Ubidots :", response_ubidots.text)

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