#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)
ultra_sensor = UltrasonicSensor(Port.S1)

TARGET_DISTANCE = 125

def print_values_ultra():
    while True:
        try:
            print("distance")
            print(ultra_sensor.distance(silent=False))
        except OSError:
            print("OSError")

while True:
    d = ultra_sensor.distance(silent=False)
    if d == TARGET_DISTANCE:
        continue
    print(d)
    speed = (d - TARGET_DISTANCE) * 2
    motor1.run(speed)
    motor2.run(speed)
