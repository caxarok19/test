import RPi.GPIO as GGG
import time

dac=[26,19,13,6,5,11,9,10]
bits = len(dac)
comporator = 4
levels = 2** bits
maxVoltage = 3.3
troykaModule = 17

def decimal2binary(value):
    return [int (bit) for bit in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = decimal2binary(value)
    GGG.output(dac,signal)
    return signal

def findbinary(a,b):
    if (b - a > 1):
        signal = num2dac(int(a + int((b - a)/2)))
        time.sleep(0.0005)
        comporatorvalue = GGG.input(comporator)
        if(comporatorvalue == 0):
            findbinary(a,a + int((b- a)/2))
        else:
            findbinary(a + int((b -a)/2), b)
    else:
        signal = num2dac(int (a + int((b - a)/2)))
        voltage = (a/levels) *maxVoltage
        indicator(voltage)
        print("ADC value = {:^3} -> {}, input voltage = {:2f}".format(a, signal, voltage)) 

def indicator (voltage):
    p = int((voltage/maxVoltage)*10)
    sig = int (2**(p-1) - 0.5) 
    out_sig = decimal2binary(sig)
    GGG.output(dac, out_sig)

 
GGG.setmode(GGG.BCM)
GGG.setup(dac, GGG.OUT, initial = GGG.LOW)
GGG.setup( troykaModule, GGG.OUT, initial = GGG.HIGH)
GGG.setup(comporator,GGG.IN)
GGG.setwarnings(False)

try:
    while True:
        findbinary(0,256)
        time.sleep(0.00007)
except KeyboardInterrupt:
    print("The program was stoped by the keyboard")

else:
    print("No exceptions")
finally:
    GGG.output(dac, GGG.LOW)
    GGG.cleanup(dac)
    print("GGG cleanup comleted")
 



    
 