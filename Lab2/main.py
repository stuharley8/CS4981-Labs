#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import math
import time

ARM1 = 12.8
ARM2 = 10.5
DEG_PER_SEC = 15

# Helper Methods
def task_one(angle_one, angle_two):
    motor1.run_target(DEG_PER_SEC, angle_one)
    motor2.run_target(DEG_PER_SEC, angle_two)


def task_two(x, y):
    move_to(x, y)


def task_three(x, y):
    lift_pen_arm()
    move_to(x, y)
    drop_pen_arm()
    mark()


def task_four(x, y, direction):
    lift_pen_arm()
    move_to(x, y)
    drop_pen_arm()
    if direction is "horizontal":
        horizontal(x, y, 10, -1)
    elif direction is "vertical":
        vertical(x, y, 10, -1)
    elif direction "diagonal":
        horizontal(x, y, 10, -1)


def task_five(x, y, shape):
    lift_pen_arm()
    move_to(x, y)
    drop_pen_arm()
    if shape is "square":
        square(x, y, 7)
    elif shape is "triangle":
        triangle(x, y, 7)


def square(x, y, d):
    vertical(x, y, d, -1)
    y = y - d
    horizontal(x, y, d, -1)
    x = x - d
    vertical(x, y, d, 1)
    y = y + d
    horizontal(x, y, d, 1)


def triangle(x, y, d):
    vertical(x, y, d, -1)
    y = y - d
    horizontal(x, y, d, -1)
    x = x - d
    diagonal(x, y, d, 1)


def horizontal(x, y, d, s):
    for i in range(0, d):
        x = x + s
        q1, q2 = two_dof_inverse_kinematics(x, y)
        motor1.run_target(10, q1)
        motor2.run_target(10, q2)
        time.sleep(1)


def vertical(x, y, d, s):
    for i in range(0, d):
        y = y + s
        q1, q2 = two_dof_inverse_kinematics(x, y)
        motor1.run_target(10, q1)
        motor2.run_target(10, q2)
        time.sleep(1)


def diagonal(x, y, d, s):
    for i in range(0, d):
        y = y + s
        x = x + s
        q1, q2 = two_dof_inverse_kinematics(x, y)
        motor1.run_target(10, q1)
        motor2.run_target(10, q2)
        time.sleep(1)


def move_to(x, y):
    angle_one, angle_two = two_dof_inverse_kinematics(x, y)
    motor1.run_target(DEG_PER_SEC, angle_one)
    motor2.run_target(DEG_PER_SEC, angle_two)


def two_dof_inverse_kinematics(x, y):
    q2 = math.degrees(math.acos((x*x+y*y-ARM1*ARM1-ARM2*ARM2)/(2*ARM1*ARM2)))
    q2neg = -math.degrees(math.acos((x*x+y*y-ARM1*ARM1-ARM2*ARM2)/(2*ARM1*ARM2)))
    q1 = math.degrees(math.atan2(y, x) - math.atan2(ARM2*math.sin(math.radians(q2)), \
        (ARM1+ARM2*math.cos(math.radians(q2)))))
    q1neg = math.degrees(math.atan2(y, x) - math.atan2(ARM2*math.sin(math.radians(q2neg)), \
        (ARM1+ARM2*math.cos(math.radians(q2neg)))))
    if q1 > 140 or q1 < 40:  # Approx Rotational limits of servo1
        q1 = q1neg
        q2 = q2neg
    elif q2 > 150 or q2 < -45:  # Approx Rotational limits of servo2
        q1 = q1neg
        q2 = q2neg
    elif q1 > q1neg:  # Angle of arm1 compared and picks the lowest
        q1 = q1neg
        q2 = q2neg
    return (q1, q2)


def drop_pen_arm():
    pen_arm.run_until_stalled(50)


def lift_pen_arm():
    pen_arm.run_until_stalled(-50)


def mark():
    time.sleep(2)
    motor2.run_time(20, 400)
    time.sleep(2)
    motor2.run_time(-20, 400)
    time.sleep(2)

# Running the Tasks
ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)
pen_arm = Motor(Port.D)

motor1.reset_angle(90)
motor2.reset_angle(0)
lift_pen_arm()

# Task 1: Test Forward Kinematics
task_one(114, 124)

# Task 2: Test Inverse Kinematics
task_two(-10.77, 2.79)

# Task 3: Mark Square Vertices
task_three(-15, 13)
task_three(-15, 8)
task_three(-10, 13)
task_three(-10, 8)

# Task 3: Mark Triangle Vertices
task_three(-7, 8)
task_three(-13, 8)
task_three(-13, 15)

# Task 4: Drawing Horizontal, Vertical, and Diagonal Lines
task_four(-2, 15, 'horizontal')
task_four(-7, 21, 'vertical')
task_four(-16, 9, 'diagonal')

# Task 5: Drawing a Square and a Triangle
task_five(-3, 18, 'square')
task_five(-5, 20, 'triangle')

lift_pen_arm()
