import serial

LIMITS = (40, 80)

class Servo:
    def __init__(self, com_port):
        self.arduino = serial.Serial(com_port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        self.arduino.write(bytes((60,)))
    
    def set_new_pos(self, pos):
        pos = LIMITS[0] if pos<LIMITS[0] else pos
        pos = LIMITS[1] if pos>LIMITS[1] else pos
        self.arduino.write(bytes((int(pos),)))