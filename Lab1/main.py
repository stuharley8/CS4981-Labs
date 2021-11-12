#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

def move(rpm, min):
    deg_per_sec = rpm / 60 * 360
    sec = min * 60
    motor1.run(deg_per_sec)
    motor2.run(deg_per_sec)
    time.sleep(sec)
    motor1.stop
    motor2.stop

def rotateCW(full_rotations, rpm=8.53, wheel_c=17.59, axle_c=37.07):
    # best rpm from past task = 8.53
    deg_per_sec = rpm / 60 * 360
    sec = full_rotations / (rpm * wheel_c / axle_c) * 60
    motor1.run(deg_per_sec)
    motor2.run(-deg_per_sec)
    time.sleep(sec)
    motor1.stop
    motor2.stop

def rotateCCW(full_rotations, rpm=8.53, wheel_c=17.59, axle_c=37.07):
    deg_per_sec = rpm / 60 * 360
    sec = full_rotations / (rpm * wheel_c / axle_c) * 60
    motor1.run(-deg_per_sec)
    motor2.run(deg_per_sec)
    time.sleep(sec)
    motor1.stop
    motor2.stop

ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)

# Task 1: Tests for 25cm
move(60, .0237)
move(8.53, .1666)
move(130, .0109)

# Task 2: Tests for rotation 90 degrees
rotateCW(.25)
rotateCCW(.25)

# Task 3: Tests for following a preprogrammed path
# Path 1 (Straight Line)
move()
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.5)
time.sleep(.5)
move()
time.sleep(.5)
move()

# Path 2 (Flag)
move()
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCCW(.25)
time.sleep(.5)
move()

# Path 3 (Hammer)
move()
time.sleep(.5)
rotateCCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCW(.25)
time.sleep(.5)
move()
time.sleep(.5)
rotateCCW(.25)
time.sleep(.5)
move()
