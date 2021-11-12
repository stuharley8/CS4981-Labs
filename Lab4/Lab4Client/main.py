#!/usr/bin/env python3
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

import time

last_turn = 'RIGHT'

#client code to be run on a pc

SERVER = '24:71:89:4a:f5:db'
def ping():
    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)

    print('establishing connection...')
    client.connect(SERVER)
    print('connected!')

    # In this program, the client sends the first message and then waits for the
    # server to reply.
    mbox.send('hello!')
    mbox.wait()
    print(mbox.read())

def sendMsg():
    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)

    print('establishing connection...')
    client.connect(SERVER)
    print('connected!')
    while 1:
        cmd = input("Enter a letter: ")
        print("Sent command was: "+cmd)
        mbox.send(cmd)

def on_path(mbox, line_color):
    actual_color = line_color
    while actual_color == line_color:
        mbox.send('drive:3,90,0')
        time.sleep(.25)
        mbox.send('query:1')
        mbox.wait()
        actual_color = mbox.read()
    mbox.send('drive:3,0,.01')
    time.sleep(.1)
    off_path(mbox, line_color, actual_color)

def off_path(mbox, line_color, actual_color):
    global last_turn
    start = time.perf_counter()
    elapsed = time.perf_counter() - start
    if last_turn == 'RIGHT':
        while actual_color != line_color and elapsed < 3.5:
            mbox.send('turn:cw,0')
            time.sleep(.05)
            elapsed = time.perf_counter() - start
            mbox.send('query:1')
            mbox.wait()
            actual_color = mbox.read()
        if actual_color == line_color:
            last_turn = 'RIGHT'
        else:
            while actual_color != line_color:
                mbox.send('turn:ccw,0')
                time.sleep(.05)
                mbox.send('query:1')
                mbox.wait()
                actual_color = mbox.read()
            last_turn = 'LEFT'
    else:
        while actual_color != line_color and elapsed < 3.5:
            mbox.send('turn:ccw,0')
            time.sleep(.05)
            elapsed = time.perf_counter() - start
            mbox.send('query:1')
            mbox.wait()
            actual_color = mbox.read()
        if actual_color == line_color:
            last_turn = 'LEFT'
        else:
            while actual_color != line_color:
                mbox.send('turn:cw,0')
                time.sleep(.05)
                mbox.send('query:1')
                mbox.wait()
                actual_color = mbox.read()
            last_turn = 'RIGHT'
    mbox.send('drive:3,0,.01')
    time.sleep(.1)
    on_path(mbox, line_color)

def client():
    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)

    print('establishing connection...')
    client.connect(SERVER)
    print('connected!')
    while 1:
        cmd = input("Enter a cmd (drive, drive_dist, turn, query, query_all, wsad or space, line_follow): ")
        if cmd == "play":
            freq = input("Enter a frequency")
            msg = cmd+":"+freq
            print("Sending message "+msg)
            mbox.send(cmd+":"+freq)
        elif cmd =="buttons":
            msg = cmd + ":" + "dummy"
            print("Sending message " + msg)
            mbox.send(msg)
            mbox.wait() #wait for a response
            b = mbox.read()
            print("lasted button pressed was "+str(b))
        elif cmd == 'drive':
            msg = cmd + ':'
            motors = input("Which motor (1 for L, 2 for R, 3 for both): ")
            msg = msg + motors
            speed = input("Enter a speed ")
            msg = msg + ',' + speed
            sec: str = input("Enter a time ")
            msg = msg + ',' + sec
            print("Sending Message: " + msg)
            mbox.send(msg)
        elif cmd == 'drive_dist':
            msg = cmd + ':'
            dist = input("Enter a distance (cm): ")
            msg = msg + dist
            print("Sending message " + msg)
            mbox.send(msg)
        elif cmd == 'turn':
            msg = cmd + ':'
            motor = input("Enter Clockwise (cw) or CounterClockwise (ccw): ")
            msg = msg + motor + ','
            degrees = input('Enter a turn angle: ')
            msg = msg + degrees
            print("Sending message: " + msg)
            mbox.send(msg)
        elif cmd == 'query':
            msg = cmd + ':'
            snum = input("Enter Sensor # 1(Color) 2(Ultrasonic) 3(Gyro) 4(Touch)")
            msg = msg + snum
            mbox.send(msg)
            mbox.wait()
            data = mbox.read()
            print("Sensor ", snum, ": ", data)
        elif cmd == 'query_all':
            while True:
                out = ''
                for i in range(4):
                    mbox.send(cmd + ':' + str(i+1))
                    mbox.wait()
                    out = out + '\tSensor ' + str(i+1) + ': ' + mbox.read()
                print(out)
                time.sleep(1)
        elif cmd == 'w':
            mbox.send('drive:3,180,0')
        elif cmd == 's':
            mbox.send('drive:3,-180,0')
        elif cmd == 'a':
            mbox.send('turn:ccw,0')
        elif cmd == 'd':
            mbox.send('turn:cw,0')
        elif cmd == ' ':
            mbox.send('drive:3,0,.01')
        elif cmd == 'line_follow':
            mbox.send('query:1')
            mbox.wait()
            line_color = mbox.read()
            on_path(mbox, line_color)
        else:
            print("Unrecognized cmd: "+cmd)


def main():
    #ping()
    #sendMsg()
    client()
if __name__ == '__main__':
    main()