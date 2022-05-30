import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(11, GPIO.OUT) ##bit 1
GPIO.setup(13, GPIO.OUT) ##bit 2
GPIO.setup(15, GPIO.OUT) ##bit 4
GPIO.setup(16, GPIO.OUT) ##bit 8

sleep = 0.2

bits=[11,13,15,16]  ##pins for bit 1,2,4,8
storePins=[12,18,22,32,29,33] ##pins for strobe on digits 1-6
blankingPins=[31,35,37,36,38,40] ##pings for blanking on digits 1-6

digitCodes =[[0,0,0,0],\
[1,0,0,0],\
[0,1,0,0],\
[1,1,0,0],\
[0,0,1,0],\
[1,0,1,0],\
[0,1,1,0],\
[1,1,1,0],\
[0,0,0,1],\
[1,0,0,1],\
]


for digit in storePins: ## initialize
	GPIO.setup(digit, GPIO.OUT) ## set pins to output
	GPIO.output(digit, GPIO.LOW)## pull low

for digit in blankingPins:
	GPIO.setup(digit, GPIO.OUT) ## set pins to output
	GPIO.output(digit, GPIO.HIGH)## pull up

#GPIO.output(blankings[0], GPIO.LOW) ##

def splitToDisplay(toDisplay):
	arrToDisplay=list(toDisplay)
	#for i in range(len(arrToDisplay)):

def unblankAll():
	for pin in blankingPins:
		GPIO.output(pin,GPIO.HIGH)
	return

def blankAll():
	for digit in blankingPins:
		GPIO.setup(digit, GPIO.OUT) ## set pins to output
		GPIO.output(digit, GPIO.LOW)## pull up

def count():

	##0
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(16, GPIO.LOW)
	time.sleep(sleep)
	##1
	GPIO.output(11, GPIO.HIGH)
	time.sleep(sleep)
	##2
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.HIGH)
	time.sleep(sleep)
	##3
	GPIO.output(11, GPIO.HIGH)
	GPIO.output(13, GPIO.HIGH)
	time.sleep(sleep)


	##4
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.HIGH)
	time.sleep(sleep)
	##5
	GPIO.output(11, GPIO.HIGH)
	#GPIO.output(12, GPIO.HIGH) ## store digit 1
	time.sleep(sleep)
	##6
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.HIGH)
	time.sleep(sleep)
	##7
	GPIO.output(11, GPIO.HIGH)
	time.sleep(sleep)

	#GPIO.output(18, GPIO.HIGH) ## store digit 2

	#8
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(16, GPIO.HIGH)
	time.sleep(sleep)

	#9
	GPIO.output(11, GPIO.HIGH)
	time.sleep(sleep*3)
	GPIO.output(blankingPins[0], GPIO.HIGH)##

def blinkPin(pin):
	GPIO.output(pin,GPIO.LOW)
	print("LOW {}".format(pin))
	time.sleep(1)
	GPIO.output(pin,GPIO.HIGH)
	print("HIGH {}".format(pin))
	time.sleep(1)

def unblank(digit):
	digit=digit-1
	print(digit)
	print(type(digit))
	#GPIO.output(blankingPins(digit), GPIO.LOW)
	return

#val=input("Enter Pin Number: ")
#unblankAll()

#blankAll()
time.sleep(2)
unblank(2)


while True:
	#blinkPin(int(val))
	#time.sleep(2)
	pass
	#count()
