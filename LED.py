import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)


rowA = 18
rowB = 6

colC = 17
colA = 27

delaytime=.1


class status:
    def __init__(self,pingTime,networkConnected,cameraON,lightsON,monitorON,clockON):
        self.pingTime=False
        self.networkConnected=False
        self.cameraON=False
        self.lightsON=False
        self.monitorON=False
        self.clockON=False

    def updateTime(pingTime):
        self.pingTime=pingTime
        print("Ping time updated to: {}").format(self.pingTime)
        return True


def init_io():
    pass


def led1(action):
    if action=="on":
        print("turning on LED1")
        GPIO.output(rowA,GPIO.HIGH)
        GPIO.output(rowB,GPIO.LOW)
        GPIO.output(colA,GPIO.LOW)
        GPIO.output(colC,GPIO.HIGH)
        time.sleep(delaytime)
    else:
        return False

def led3(action):
    if action=="on":
        print("turning on LED3")
        GPIO.output(rowA,GPIO.HIGH)
        GPIO.output(rowB,GPIO.LOW)
        GPIO.output(colA,GPIO.HIGH)
        GPIO.output(colC,GPIO.LOW)
        time.sleep(delaytime)
    else:
        return False


led1('on')




while True:
    
    led1('on')
    led3('on')
