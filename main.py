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

# SKIP

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
    time.sleep(0.5)