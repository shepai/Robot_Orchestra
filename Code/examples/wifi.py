import os
import ipaddress
import wifi
import socketpool
import time
from droid_class import Droid

d=Droid()

print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)
#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)


