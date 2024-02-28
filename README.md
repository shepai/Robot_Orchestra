# Robot_Orchestra
Code for controlling the robot orchestra chassis. This makes use of two DC motors and 14 servos, two arms and one neck.

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

- CircuitPython libraries.
- Adafruit CircuitPython PCA9685 library.
- Adafruit CircuitPython ServoKit library.

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
