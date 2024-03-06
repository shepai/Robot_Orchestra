# Robot_Orchestra
Code for controlling the robot orchestra chassis. This makes use of two DC motors and 14 servos, two arms and one neck. We hacked a turtle robot chassis, but anything with two DC motors will do. On top we mount a 14 degrees of freedom body. The controlling of the library is seen in the class documentation listed below. We have included plenty of <a href="https://github.com/shepai/Robot_Orchestra/tree/main/Code/examples">examples</a>

# Droid Class Documentation

## Introduction

The `Droid` class is a Python class designed for controlling a robot using CircuitPython, the Adafruit PCA9685 16-Channel PWM/Servo Driver, and various other components. This class encapsulates functionality for servo motor control, DC motor control, and sensor readings.

## Hardware Requirements

1. CircuitPython-compatible microcontroller board.
2. Adafruit PCA9685 16-Channel PWM/Servo Driver.
3. Servo motors.
4. DC motors.
5. Multiplexer for sensor readings.
6. Analog and digital pins for wiring.

## Dependencies

CircuitPython libraries.
- Adafruit CircuitPython PCA9685 library.
- Adafruit CircuitPython ServoKit library.
- Adafruit ht16k33
- Adafruit register
- Adafruit motorkit
- Adafruit_motor

In order to get the wifi working you will need to save a file called <a href="https://learn.adafruit.com/pico-w-wifi-with-circuitpython/create-your-settings-toml-file">settings.toml</a> with the following content:
```
CIRCUITPY_WIFI_SSID = "wifi name"
CIRCUITPY_WIFI_PASSWORD = "wifi password"
```

For the PC side we make use of TKinter and sockets, that should both be installed by default with Python.

## Class Initialization

```python
droid = Droid()
```

The initialization of the `Droid` class sets up the required hardware components, initializes the PCA9685 driver, and prepares the servo motors, DC motors, and sensors.

## Servo Motor Control

### `setMotors(positions, step_size=2)`

Sets the positions of servo motors gradually.

- `positions`: List of target positions for each servo.
- `step_size`: Step size for each movement (default is 2).

The motor positions of each of the motors corrosponds as following:

```
[right hand, right wrist rotate, right wrist, right elbow, right shoulder, right shoulder rotate, neck, neck rotate, left shoulder rotate, left shoulder, left elbow, left wrist, left wrist rotate, left hand]
```

### `set_specific(channel, position)`

Sets a specific servo to a specified position.

- `channel`: Servo channel index.
- `position`: Target position for the servo.

### `neutral()`

Moves all servo motors to a neutral position.

## DC Motor Control

### `forward(speed=1.0)`

Moves the robot forward.

- `speed`: Speed of movement (default is 1.0).

### `backward(speed=1.0)`

Moves the robot backward.

- `speed`: Speed of movement (default is 1.0).

### `left(speed=1.0)`

Turns the robot left.

- `speed`: Speed of turning (default is 1.0).

### `right(speed=1.0)`

Turns the robot right.

- `speed`: Speed of turning (default is 1.0).

### `stop()`

Stops all DC motors.

## Sensor Readings

### `readPositions()`

Reads analog sensor values from the multiplexer for each channel.

Returns a list of sensor values.

## Additional Methods

### `select_channel(channel)`

Selects a specific channel on the multiplexer.

- `channel`: Channel index to be selected.

### `_set_motor_speed(motor_pwm, speed)`

Sets the speed of a DC motor.

- `motor_pwm`: PWMOut object representing the motor's PWM pin.
- `speed`: Speed of the motor (0.0 to 1.0).

### `_set_motor_direction(motor_out1, motor_out2, direction)`

Sets the direction of a DC motor.

- `motor_out1`: DigitalInOut object representing one direction pin.
- `motor_out2`: DigitalInOut object representing the other direction pin.
- `direction`: Direction of the motor (1 for forward, -1 for backward).


# examples
There are many examples provided in this repository. Some are for running on device, allowing you to modify the existing robot code.
The PC side code is designed for network communication with the robot wirelessly. The code on the robot will need to be running the <a href="https://github.com/shepai/Robot_Orchestra/blob/main/Code/examples/wifi.py">wifi.py</a> which waits for a connection to the server. Bare in mind that the ip address of the server will need to be changed in wifi.py to match the ip of your device hosting.

To run the server you can use either of the examples. GUI allows you to control the robot via a graphical interface. The server code is more basic but is easier to modify.

The WiFi code works by sending bytearrays to the device. These bytearrays have a command, that is sometimes followed by values. The way these instructions work is as follows

## Commands

To go forward send the string:
```
forward
```
To go backward send the string:
```
backward
```
To go left send the string:
```
left
```
To go right send the string:
```
right
```
To stop send the string:
```
stop
```
Move motors at the same time. The following will send all servo commands to 0 degrees. The final position is for the wheels. 0 to not move, 1 to go forward, 2 for backwards, 3 for left and 4 for right.
```
set[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
```
Go backwards:
```
set[0,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
```
Set neutral pose:
```
set[150,150,100,110,50,40,100,100,180,40,180,40,50,100,0]
```

