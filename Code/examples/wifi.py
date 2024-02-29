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



# Specify the server's IP address and port
server_ip = "192.168.1.27"  # Replace with the server's IP address
server_port = 12345

# Create a socket using the pool
sock = pool.socket()
addr = pool.getaddrinfo(server_ip, server_port)[0][-1]
sock.connect(addr)
sock.send(b"Hello, server!")

while True:
    # Send data to the server
    data = bytearray(20)    
    a = sock.recvfrom_into(data)
    command=data.decode("uft-8")
    command=command.replace(" ","")
    if "exit" in command:
        break
    elif "set" in command:
        command=command.replace("set")
        
    else:
        print(command)
    # Close the socket
sock.close()

