import os
import ipaddress
import wifi
import socketpool
import time
from droid_class import Droid

d=Droid()
d.neutral()
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
    try:
        # Send data to the server
        data = bytearray(100)    
        a = sock.recvfrom_into(data)
        command=data.decode("uft-8")
        command=command.replace(" ","").rstrip('\x00')
        print("command:",command)
        if "exit" in command:
            break
        elif "set" in command:
            command=command.replace("set","").replace("[","").replace("]","")
            ar=command.split(",")
            print(ar)
            mov=[int(ar[i]) for i in range(len(ar))]
            print(mov)
            d.setMotors(mov)
        elif "forward" in command:
            d.forward(0.5)
        elif "stop" in command:
            d.stop()
        elif "left" in command:
            d.left(0.5)
        elif "right" in command:
            d.right(0.5)
        elif "backward" in command:
            d.backward(0.5)
        else:
            print(command)
    except OSError:
        sock = pool.socket()
        addr = pool.getaddrinfo(server_ip, server_port)[0][-1]
        sock.connect(addr)
# Close the socket
d.stop()
d.neutral()
sock.close()

