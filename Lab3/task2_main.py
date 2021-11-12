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
last_turn = 'RIGHT'

ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)
color_sensor = ColorSensor(Port.S1)

def test_print_colors():
    while True:
        try:
            print(color_sensor.color())
            time.sleep(.5)
        except OSError:
            print("OSError")

def on_path():
    while color_sensor.color() is Color.WHITE:
        motor1.run(DEG_PER_SEC)
        motor2.run(DEG_PER_SEC)
    time.sleep(.1)
    off_path()

def off_path():
    global last_turn
    start = time.perf_counter()
    elapsed = time.perf_counter() - start
    if last_turn is 'RIGHT':
        while color_sensor.color() is not Color.WHITE and elapsed < 3.5:
            motor1.run(DEG_PER_SEC)
            motor2.run(-DEG_PER_SEC)
            elapsed = time.perf_counter() - start
        if color_sensor.color() is Color.WHITE:
            last_turn = 'RIGHT'
        else:
            while color_sensor.color() is not Color.WHITE:
                motor1.run(-DEG_PER_SEC)
                motor2.run(DEG_PER_SEC) 
                last_turn = 'LEFT'
    else:
        while color_sensor.color() is not Color.WHITE and elapsed < 3.5:
            motor1.run(-DEG_PER_SEC)
            motor2.run(DEG_PER_SEC)
            elapsed = time.perf_counter() - start
        if color_sensor.color() is Color.WHITE:
            last_turn = 'LEFT'
        else:
            while color_sensor.color() is not Color.WHITE:
                motor1.run(DEG_PER_SEC)
                motor2.run(-DEG_PER_SEC) 
                last_turn = 'RIGHT'
    time.sleep(.1)
    on_path()

  
on_path()