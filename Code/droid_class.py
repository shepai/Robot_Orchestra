import time
from adafruit_servokit import ServoKit
import board
import busio


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
    def setMotors(self,positions):
        assert len(positions)==len(self.kit.servo)-2, "Incorrect sizes"
        for i in range(len(self.positions)):
            self.kit.servo[self.positions[i]].angle=positions[i]
            print("motor",self.positions[i],"to",positions[i])
    def readPositions(self):
        pass


d=Droid()
d.setMotors([90 for i in range(14)])
time.sleep(2)
for i in range(30):
    d.setMotors([132+i for i in range(14)])
    time.sleep(0.1)
