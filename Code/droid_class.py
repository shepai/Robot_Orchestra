import time
from adafruit_servokit import ServoKit
import board
import busio
import digitalio
import analogio

class Droid:
    def __init__(self):  
        i2c = busio.I2C(board.GP17, board.GP16)
        while not i2c.try_lock():
            pass
        print("I2C addresses found:",[hex(device_address) for device_address in i2c.scan()])
        time.sleep(2)
        i2c.unlock()

        # Initialize the ServoKit object with the i2c address of the PCA9685
        self.kit = ServoKit(channels=16,i2c=i2c)
        self.positions=[0,1,2,3,4,5,7,8,10,11,12,13,14,15]
        #setup multiplexer
        mux_select_pins = [board.GP0, board.GP1, board.GP2, board.GP3]
        self.signal_pin = analogio.AnalogIn(board.GP26)
        self.mux_select = [digitalio.DigitalInOut(pin) for pin in mux_select_pins]
        for pin in self.mux_select:
            pin.direction = digitalio.Direction.OUTPUT
    def setMotors(self,positions):
        assert len(positions)==len(self.kit.servo)-2, "Incorrect sizes"
        for i in range(len(self.positions)):
            self.kit.servo[self.positions[i]].angle=positions[i]
            print("motor",self.positions[i],"to",positions[i])
            time.sleep(0.1)
    def select_channel(self,channel):
        for i, pin in enumerate(self.mux_select):
            pin.value = (channel >> i) & 1
    def readPositions(self):
        arr=[]
        for i in range(14):
            self.select_channel(i)
            analog_value = self.signal_pin.value
            arr.append(analog_value)
        return arr


d=Droid()
for i in range(10000):
    print(d.readPositions()[1])

