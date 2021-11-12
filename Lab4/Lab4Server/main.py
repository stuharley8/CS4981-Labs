#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

from _thread import allocate_lock

import time

DEG_PER_SEC = 90
RUN_TIME_PER_CM = .235
TURN_TIME_PER_DEG = .023

# Create your objects here.
ev3 = EV3Brick()
motor1 = Motor(Port.B)
motor2 = Motor(Port.C)
s1_sensor = ColorSensor(Port.S1)
s2_sensor = UltrasonicSensor(Port.S2)
s3_sensor = GyroSensor(Port.S3)
s4_sensor = TouchSensor(Port.S4)

# Write your program here.
ev3.speaker.beep()

#Note the timeout parameter doesn't seem to work
#This wait checks for a message and then just returns
#Compared to wait() which will sit there and wait
#for a message
def wait_with_timeout(mbox,name):
        """Waits until ``mbox`` receives a value."""
        lock = allocate_lock()
        lock.acquire()
        with mbox._connection._lock:
            mbox._connection._updates[name] = lock
        try:
            #timeout parameter doesn't work as
            #expected so I'm just setting
            #the wait flag to be zero
            return lock.acquire(0,1)
        finally:
            with mbox._connection._lock:
                del mbox._connection._updates[name]

def ping():
    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)

    # The server must be started before the client!
    print('waiting for connection...')
    server.wait_for_connection()
    print('connected!')

    # In this program, the server waits for the client to send the first message
    # and then sends a reply.
    mbox.wait()
    print(mbox.read())
    mbox.send('hello to you!')

def setupConnection():
    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)

    # The server must be started before the client!
    print('waiting for connection...')
    server.wait_for_connection()
    print('connected!')
    return mbox

def receiveMsg():
    mbox = setupConnection()
    while 1:
        mbox = setupConnection()
        mbox.wait()
        msg = mbox.read()
        print("Message received is: "+msg)
        if msg == "q":
            break            

def playNotes():
    mbox = setupConnection()

    while 1:
        wait_with_timeout(mbox,mbox.name)
        msg = mbox.read()
        if msg != None:
            print("Message received is: "+msg)
            if msg == "q":
                break
            elif msg == "a":
                ev3.speaker.beep(880,100)
            elif msg == "c":
                ev3.speaker.beep(523,100)
            elif msg == "g":
                ev3.speaker.beep(783,100)
            mbox._connection._mailboxes={}
            msg = None

def server():
    mbox = setupConnection()
    pressed = ""
    while 1:
        wait_with_timeout(mbox,mbox.name) #non-blocking
        #wait() #blocking
        msg = mbox.read()
        #if pressed != []:
        #    print("pressed  is "+str(pressed))
        if msg != None:
            print("Message received is: "+msg)
            #assumes there are only two tokens
            cmd,arg = mbox.read().split(":")
            if cmd == "play":
                #print("arg is "+arg)
                if arg == "q":
                    break
                elif arg == "a":
                    ev3.speaker.beep(880,100)
                elif arg == "c":
                    ev3.speaker.beep(523,100)
                elif arg == "g":
                    ev3.speaker.beep(783,100)
            elif cmd == "buttons":
                #print("pressed is "+str(pressed))
                mbox.send(pressed)
            elif cmd == "drive":
                motor, speed, runtime = arg.split(',')
                speed = float(speed)
                runtime = float(runtime)
                if motor is '1':
                    motor1.run(speed)
                elif motor is '2':
                    motor2.run(speed)
                elif motor is '3':
                    motor1.run(speed)
                    motor2.run(speed)
                if int(runtime) is not 0:
                    time.sleep(runtime)
                    motor1.brake()
                    motor2.brake()
            elif cmd == "drive_dist":
                dist = float(arg)
                motor1.run(DEG_PER_SEC)
                motor2.run(DEG_PER_SEC)
                time.sleep(dist * RUN_TIME_PER_CM)
                motor1.brake()
                motor2.brake()
            elif cmd == "turn":
                direction, degrees = arg.split(',')
                runtime = float(degrees) * TURN_TIME_PER_DEG
                if direction is 'cw':
                    motor1.run(DEG_PER_SEC)
                    motor2.run(-DEG_PER_SEC)
                elif direction is 'ccw':
                    motor1.run(-DEG_PER_SEC)
                    motor2.run(DEG_PER_SEC)
                if int(degrees) is not 0:
                    time.sleep(runtime)
                    motor1.brake()
                    motor2.brake()
            elif cmd == "query" or "query_all":
                data = None
                if arg is '1': # Color sensor
                    data = s1_sensor.color()
                elif arg is '2': # Ultrasonic sensor
                    data = s2_sensor.distance()
                elif arg is '3': # Gyroscope sensor
                    data = s3_sensor.speed()
                elif arg is '4': # Touch sensor
                    data = s4_sensor.pressed()
                mbox.send(data)
            else:
                print("Received invalid cmd "+cmd)
            #clears msg and the mailbox
            msg = None
            mbox._connection._mailboxes={}
        
        buttons = ev3.buttons.pressed()
        #gets the buttons pressed if any
        if buttons != []:
            pressed = "" #clears pressed
            for i in range(len(buttons)):
                pressed+=str(buttons[i])
                if i!=len(buttons)-1:
                    pressed+=":"
                    

def printButtons():
    pressed = ""
    while True:
        buttons = ev3.buttons.pressed()
        print(buttons)
        #gets the buttons pressed if any
        if buttons != []:
            pressed = "" #clears pressed
            for i in range(len(buttons)):
                pressed+=str(buttons[i])
                if i!=len(buttons)-1:
                    pressed+=":"
        print("Pressed is "+pressed)
def main():
    #receiveMsg()
    #playNotes()
    server()
    #printButtons()

if __name__ == '__main__':
    main()
