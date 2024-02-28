import time
from adafruit_servokit import ServoKit
import board
import busio
import digitalio
import analogio
import pwmio
import board
from adafruit_ht16k33.matrix import Matrix8x8
eyeshape=[[0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0],
          [0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
          [1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1],
          [1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1],
          [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
          [0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
          [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0]]

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
        self.signal_pin = analogio.AnalogIn(board.GP27)
        self.mux_select = [digitalio.DigitalInOut(pin) for pin in mux_select_pins]
        for pin in self.mux_select:
            pin.direction = digitalio.Direction.OUTPUT
        self.validate={8:[0,180],}
        self.start=[150,150,100,110,50,40,100,100,180,40,180,40,50,100]
        #make eyes
        self.eye1 = Matrix8x8(i2c, address=(0x70))
        self.eye1.brightness = 0.4
        self.eye1.fill(1)
        self.eye2 = Matrix8x8(i2c, address=(0x72))
        self.eye2.brightness = 0.4
        self.eye2.fill(1)
        self.parse_eyes(eyeshape)
        #dc motors
        motor1_pwm=board.GP19
        motor2_pwm=board.GP18
        motor1_out1=board.GP21
        motor1_out2=board.GP20
        motor2_out1=board.GP14
        motor2_out2=board.GP15
        
        self.motor1_pwm = pwmio.PWMOut(motor1_pwm, frequency=1000, duty_cycle=0)
        self.motor1_out1 = digitalio.DigitalInOut(motor1_out1)
        self.motor1_out1.direction = digitalio.Direction.OUTPUT
        self.motor1_out2 = digitalio.DigitalInOut(motor1_out2)
        self.motor1_out2.direction = digitalio.Direction.OUTPUT

        # Motor 2 setup
        self.motor2_pwm = pwmio.PWMOut(motor2_pwm, frequency=1000, duty_cycle=0)
        self.motor2_out1 = digitalio.DigitalInOut(motor2_out1)
        self.motor2_out1.direction = digitalio.Direction.OUTPUT
        self.motor2_out2 = digitalio.DigitalInOut(motor2_out2)
        self.motor2_out2.direction = digitalio.Direction.OUTPUT
    def parse_eyes(self,matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.eye1[i, j] = matrix[i][j]
                self.eye2[i, j] = matrix[i][j+8]
    def setMotors(self,positions,step_size=2):
        assert len(positions)==len(self.kit.servo)-2, "Incorrect sizes"
        iterators=[] 
        for i,idx in enumerate(self.positions): #gather movement instructions
            try:
                current_angle=int(self.kit.servo[idx].angle)
            except:
                current_angle=positions[i]-2
            iterator=list(range(current_angle,positions[i],step_size))
            if current_angle>positions[i]: iterator=list(reversed(range(positions[i],current_angle,step_size)))
            if len(iterator)>0:
                iterators.append([idx,iterator])
        c=0
        while len(iterators)>0: #keep following instructions till all done
            to_pop=[]
            for i in range(len(iterators)):
                if c<len(iterators[i][1]):
                    next_value=iterators[i][1][c]
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
        if len(self.validate.get(channel,[]))>0: #check within bounds
            if position>self.validate[channel][1]:
                position=self.validate[channel][1]
            elif position<self.validate[channel][0]:
                position=self.validate[channel][0]
        self.kit.servo[channel].angle=position
    def select_channel(self,channel):
        for i, pin in enumerate(self.mux_select):
            pin.value = int((channel >> i) & 1)
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
    def _set_motor_speed(self, motor_pwm, speed):
        # Map speed from the range [-1, 1] to [0, 65535]
        mapped_speed = int((speed + 1) / 2 * 65535)
        motor_pwm.duty_cycle = mapped_speed

    def _set_motor_direction(self, motor_out1, motor_out2, direction):
        motor_out1.value = direction == 1
        motor_out2.value = direction == -1

    def backward(self, speed=1.0):
        self._set_motor_speed(self.motor1_pwm, speed)
        self._set_motor_speed(self.motor2_pwm, speed)
        self._set_motor_direction(self.motor1_out1, self.motor1_out2, 1)
        self._set_motor_direction(self.motor2_out1, self.motor2_out2, 1)

    def forward(self, speed=1.0):
        self._set_motor_speed(self.motor1_pwm, speed)
        self._set_motor_speed(self.motor2_pwm, speed)
        self._set_motor_direction(self.motor1_out1, self.motor1_out2, -1)
        self._set_motor_direction(self.motor2_out1, self.motor2_out2, -1)

    def left(self, speed=1.0):
        self._set_motor_speed(self.motor1_pwm, speed)
        self._set_motor_speed(self.motor2_pwm, speed)
        self._set_motor_direction(self.motor1_out1, self.motor1_out2, 1)
        self._set_motor_direction(self.motor2_out1, self.motor2_out2, -1)

    def right(self, speed=1.0):
        self._set_motor_speed(self.motor1_pwm, speed)
        self._set_motor_speed(self.motor2_pwm, speed)
        self._set_motor_direction(self.motor1_out1, self.motor1_out2, -1)
        self._set_motor_direction(self.motor2_out1, self.motor2_out2, 1)

    def stop(self):
        self._set_motor_speed(self.motor1_pwm, 0)
        self._set_motor_speed(self.motor2_pwm, 0)
        self._set_motor_direction(self.motor1_out1, self.motor1_out2, 0)
        self._set_motor_direction(self.motor2_out1, self.motor2_out2, 0)

