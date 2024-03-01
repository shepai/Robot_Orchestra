import socket
import time
import tkinter as tk

class RobotConnection:
    def __init__(self):
        # Get the local machine's hostname
        hostname = socket.gethostname()
        # Set the host and port to listen on
        self.host = socket.gethostbyname(hostname)
        self.port = 12345
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a specific address and port
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen()
        self.client_socket=None
        self.client_address=None
        print("Server hosting on",self.host)
    def search(self):
        # Accept a connection from a client
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Connection established with {client_address}")
    def sendMessage(self,string):
        try:
            self.client_socket.send(string.encode())
            return True
        except ConnectionResetError:
            pass
        except ConnectionResetError:
            pass
        return False

class interface:
    def __init__(self,server):
        self.server=server
        self.defaults=[150,150,100,110,50,40,100,100,180,40,180,40,50,100]
        self.create()
    def create(self):
        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("GUI with Connect Button and 14 Sliders")

        # Connect Button
        connect_button = tk.Button(self.root, text="Connect", command=self.on_connect_button_click)
        connect_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Sliders
        num_sliders = 14
        self.slider_vars = []

        for i in range(num_sliders):
            slider_label = tk.Label(self.root, text=f"Slider {i + 1} Value:")
            slider_label.grid(row=i + 1, column=0, sticky=tk.E)

            var = tk.IntVar()
            var.set(self.defaults[i])
            self.slider_vars.append(var)

            slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, variable=var)
            slider.grid(row=i + 1, column=1)
            slider.bind("<B1-Motion>", lambda event, i=i+1: self.on_slider_change(i))
        # Movement Buttons
        forward_button = tk.Button(self.root, text="Forward", command=self.move_forward)
        forward_button.grid(row=num_sliders + 2, column=0, pady=5)

        left_button = tk.Button(self.root, text="Left", command=self.move_left)
        left_button.grid(row=num_sliders + 3, column=0, pady=5)

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_movement)
        stop_button.grid(row=num_sliders + 3, column=1, pady=5)

        right_button = tk.Button(self.root, text="Right", command=self.move_right)
        right_button.grid(row=num_sliders + 3, column=2, pady=5)

        backward_button = tk.Button(self.root, text="Backward", command=self.move_backward)
        backward_button.grid(row=num_sliders + 4, column=0, columnspan=3, pady=5)

        # Send Button on the right side
        send_button = tk.Button(self.root, text="Send", command=self.on_send_button_click)
        send_button.grid(row=num_sliders + 5, column=2, sticky=tk.E)
    def run(self):
        # Run the Tkinter event loop
        self.root.mainloop()

    def on_connect_button_click(self):
        try:
            self.server.search()
        except:
            pass

    def on_slider_change(self,slider_id):
        value = self.slider_vars[slider_id - 1].get()
        #print(f"Slider {slider_id} Value: {value}")

    def on_send_button_click(self):
        ar=[]
        for i in range(len(self.slider_vars)):
            ar.append(self.slider_vars[i].get())
        self.server.sendMessage("set"+str(ar))
    def move_forward(self):
        self.server.sendMessage("forward")

    def move_left(self):
        self.server.sendMessage("left")

    def move_right(self):
        self.server.sendMessage("right")

    def move_backward(self):
        self.server.sendMessage("backward")

    def stop_movement(self):
        self.server.sendMessage("stop")


server=RobotConnection()
gui=interface(server)
gui.run()
