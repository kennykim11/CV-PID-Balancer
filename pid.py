"""
PV = Process Variable – a quantity used as a feedback, typically measured by an instrument. Also sometimes called “MV” – Measured Value.
SP = SetPoint – the desired value for the PV.
OP = OutPut – a signal to a device that can change the PV – frequently a valve, damper, or a pump speed reference.   Often called “CV” – Controlled Value.
Overshoot = when the PV moves further past the SP than desired.
"""
from time import time

def pid(kP, kI, kD, setpoint, processVar):
    old_time = time()
    last_error = 0
    I = 0
    while True:
        error = setpoint - processVar
        new_time = time()
        time_diff = (new_time - old_time) or 1

        P = kP * error
        I += kI * error * time_diff
        D = kD * (error-last_error) / time_diff
        output = P+I+D
        print(f'{P=:7.2f},     {I=:7.2f},     {D=:7.2f},     {setpoint=:7.2f},     {processVar=:7.2f},     {output=:7.2f}')

        last_error = error
        old_time = new_time
        
        processVar = yield output
