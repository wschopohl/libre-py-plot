import serial
import time
import json
from mppt_controller import MPPTController
import threading
import datetime as dt

datahistory = []
received = False

running = True

ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port

def gather():
    global received, datahistory
    

    while running:
        line = ser.readline().decode("utf-8")
        line = line.replace("#mSerial ", "")
        try:
            data = json.loads(line)
            mppt = MPPTController(data)
            #datahistory.append(mppt)
            datahistory = [mppt]
            received = True
        except json.decoder.JSONDecodeError:
            pass
    
        time.sleep(0.1)

x = threading.Thread(target=gather)

def toggle_load():
    if not received: return
    cmd = b'=Load {"wEnable":false}\n'
    if datahistory[-1].load_state == 0:
        cmd = b'=Load {"wEnable":true}\n'
    ser.write(cmd)

def start_sweep():
    if not received: return
    cmd = b'!Device/xSweep\n'
    ser.write(cmd)


def stop():
    global running
    running = False
    x.join()
    ser.close() 


def start():
    x.start()