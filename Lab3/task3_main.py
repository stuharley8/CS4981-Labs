#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

DEG_PER_SEC = 90

ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)
left_sensor = TouchSensor(Port.S1)
right_sensor = TouchSensor(Port.S4)

def test_touch_sensors():
    while True:
        try:
            print('Left Pressed: ', left_sensor.pressed())
            print('Right Pressed: ', right_sensor.pressed())
            time.sleep(2)
        except OSError:
            print("OSError")

def rotateCW(full_rotations, rpm=8.53, wheel_c=17.59, axle_c=37.07):
    deg_per_sec = rpm / 60 * 360
    sec = full_rotations / (rpm * wheel_c / axle_c) * 60
    motor1.run(deg_per_sec)
    motor2.run(-deg_per_sec)
    time.sleep(sec+.9)
    motor1.stop
    motor2.stop

def rotateCCW(full_rotations, rpm=8.53, wheel_c=17.59, axle_c=37.07):
    deg_per_sec = rpm / 60 * 360
    sec = full_rotations / (rpm * wheel_c / axle_c) * 60
    motor1.run(-deg_per_sec)
    motor2.run(deg_per_sec)
    time.sleep(sec+1)
    motor1.stop
    motor2.stop

def on_wall():
    start = time.perf_counter()
    elapsed = time.perf_counter() - start
    motor1.run(DEG_PER_SEC)
    motor2.run(DEG_PER_SEC)
    while not left_sensor.pressed() and not right_sensor.pressed() and elapsed < 3:
        elapsed = time.perf_counter() - start
    motor1.brake()
    motor2.brake()
    if left_sensor.pressed() or right_sensor.pressed():
        hit_wall()
    else:
        check_wall_right()

def check_wall_right():
    rotateCW(.25)
    start = time.perf_counter()
    elapsed = time.perf_counter() - start
    motor1.run(DEG_PER_SEC)
    motor2.run(DEG_PER_SEC)
    while not left_sensor.pressed() and not right_sensor.pressed() and elapsed < 2:
        elapsed = time.perf_counter() - start
    motor1.brake()
    motor2.brake()
    if left_sensor.pressed() or right_sensor.pressed():
        hit_wall()
    else:
        on_wall()

def hit_wall():
    motor1.run(-DEG_PER_SEC)
    motor2.run(-DEG_PER_SEC)
    time.sleep(.5)
    motor1.brake()
    motor2.brake()
    rotateCCW(.25)
    on_wall()

on_wall()