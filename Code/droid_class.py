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
        self.validate={8:[120,180],}
        self.start=[150,150,100,110,50,40,100,180,180,40,180,40,50,100]
    def setMotors(self,positions,step_size=2):
        assert len(positions)==len(self.kit.servo)-2, "Incorrect sizes"
        iterators=[] 
        for i,idx in enumerate(self.positions): #gather movement instructions
            current_angle=int(self.kit.servo[idx].angle)
            iterator=list(range(current_angle,positions[i],step_size))
            if current_angle>positions[i]: iterator=list(reversed(range(positions[i],current_angle,step_size)))
            if len(iterator)>0:
                iterators.append([idx,i,iterator])
        c=0
        while len(iterators)>0: #keep following instructions till all done
            to_pop=[]
            for i in range(len(iterators)):
                if c<len(iterators[i][2]):
                    next_value=iterators[i][2][c]
                    validate=True
                    index=iterators[i][0]
                    if len(self.validate.get(index,[]))>0: #check within bounds
                        if not(next_value>=self.validate[index][0] and next_value<=self.validate[index][1]):
                            validate=False
                    if validate:
                        if next_value>180: next_value=180
                        if next_value<0: next_value=0
                        self.kit.servo[index].angle=next_value
                else:
                    to_pop.append(i)
            c+=1
            i=0
            while i<len(to_pop): #kill finished streams
                iterators.pop(list(reversed(to_pop))[i])
                i+=1
        time.sleep(0.1)
            
    def set_specific(self,channel,position):
        self.kit.servo[channel].angle=position
    def select_channel(self,channel):
        for i, pin in enumerate(self.mux_select):
            pin.value = (channel >> i) & 1
        #print(channel,[self.mux_select[i].value for i in range(4)])
    def readPositions(self):
        arr=[]
        for i in range(14):
            self.select_channel(i)
            analog_value = self.signal_pin.value
            arr.append(analog_value)
        return arr
    def neutral(self):
        self.setMotors(self.start)

d=Droid()
for i in range(10000):
    print(d.readPositions()[0])


