import socket
import time

# Get the local machine's hostname
hostname = socket.gethostname()
# Set the host and port to listen on
host = socket.gethostbyname(hostname)
port = 12345
print(host)
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {host}:{port}")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")
t=time.time()
while time.time()-t<1000:
    # Send a message to the client
    try:
        message = input("Command to robot>")
        if message=="1": #command
            client_socket.send(("set"+str([100 for i in range(14)])).encode())
        elif message=="2":
            a=[]
            for i in range(14): #allo the user to manually enter values
                a.append(int(input("Motor "+str(i+1)+" value>")))
            client_socket.send(("set"+str([100 for i in range(14)])).encode())
        elif message=="3": #forard
            client_socket.send(("forward").encode())
        elif message=="4": #stop
            client_socket.send(("stop").encode())
        elif message=="5": #left
            client_socket.send(("left").encode())
        elif message=="6": #right
            client_socket.send(("right").encode())
        else:
            client_socket.send(message.encode())
        time.sleep(1)
    except ConnectionResetError:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
    except ConnectionAbortedError:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
# Close the sockets
client_socket.close()
server_socket.close()
