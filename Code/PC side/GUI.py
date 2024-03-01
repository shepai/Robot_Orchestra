import socket
import time
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import numpy as np

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
        self.loadedFile=np.array([np.array(self.defaults).copy()])
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

            slider = tk.Scale(self.root, from_=0, to=180, orient=tk.HORIZONTAL, variable=var)
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

        #play
        send_button = tk.Button(self.root, text="Record", command=self.record)
        send_button.grid(row=num_sliders + 5, column=3, sticky=tk.E)

        #record
        send_button = tk.Button(self.root, text="Play", command=self.play)
        send_button.grid(row=num_sliders + 5, column=4, sticky=tk.E)
        #reset
        send_button = tk.Button(self.root, text="Reset", command=self.reset)
        send_button.grid(row=num_sliders + 6, column=4, sticky=tk.E)
        
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_command(label="Save current order", command=self.savefile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)
        self.writings=[]
    def reset(self):
        self.loadedFile=np.array([np.array(self.defaults).copy()])
    def play(self,delay=0.5):
        print("play")
        for i in range(len(self.loadedFile)):
            positions=list(self.loadedFile[i])
            time.sleep(delay)
            try:
                self.server.sendMessage("set"+str(positions)) #send positions to robot
            except:
                print("set"+str(positions))
            for j in range(len(self.slider_vars)): #update gui positions
                self.slider_vars[j].set(positions[j])
        print("Done")
    def record(self):
        print("record")
        ar=[]
        for i in range(len(self.slider_vars)):
            ar.append(self.slider_vars[i].get())
        ar=np.array(ar)
        self.loadedFile=np.vstack([self.loadedFile,ar])
        print(self.loadedFile)
    def openfile(self): #open a sequence
        filename = askopenfilename()
        self.loadedFile = np.loadtxt(filename,
                 delimiter=",", dtype=float).astype(int)
        print("loaded file",self.loadedFile)
    def savefile(self): #save a sequence
        f=asksaveasfile(defaultextension=".csv")
        print(f.name)
        np.savetxt(f.name, self.loadedFile, delimiter=",") #csv format
    def on_closing(self):
        self.root.destroy()
        try:
            self.server.sendMessage("exit")
        except:
            pass
    def run(self):
        # Run the Tkinter event loop
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
