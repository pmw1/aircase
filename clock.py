import RPi.GPIO as GPIO
import time
import datetime
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(11, GPIO.OUT) ##bit 1
GPIO.setup(13, GPIO.OUT) ##bit 2
GPIO.setup(15, GPIO.OUT) ##bit 4
GPIO.setup(16, GPIO.OUT) ##bit 8

sleep = 0.5

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


def latch(digitPosition):
	GPIO.output(storePins[digitPosition], GPIO.HIGH)
	return

def unlatch(digitPosition):
	GPIO.output(storePins[digitPosition], GPIO.LOW)
	return

def latchAll():
	for pin in range(0,5):
		latch(pin)

def unlatchAll():
	for pin in range(0,5):
		unlatch(pin)

def setDigit(digitPosition,displayNumber):

	unlatch(digitPosition)

	##### Process number to display
	code=digitCodes[displayNumber]
	#print(code)
	for i in range(0,len(code)):
		#print("{}: {}".format(i, code[i]))
		if code[i] == 1:
			GPIO.output(bits[i], GPIO.HIGH)
		elif code[i] == 0:
			GPIO.output(bits[i], GPIO.LOW)

	latch(digitPosition)

	# for bit in digitCodes[displayNumber]:
	# 	if bit == 1:
	# 		GPIO.output(bits[displayNumber](bit), GPIO.HIGH)
	# 	elif bit == 0:
	# 		GPIO.output(bits[displayNumber](bit), GPIO.LOW)
	# 	else: return False

def unblankAll():
	for pin in blankingPins:
		GPIO.output(pin,GPIO.HIGH)
	return

def blankAll():
	for digit in blankingPins:
		GPIO.setup(digit, GPIO.OUT) ## set pins to output
		GPIO.output(digit, GPIO.LOW)## pull up

def blankDigit(digit):
	GPIO.setup(blankingPins[digit], GPIO.LOW)
	return

def unblankDigit(digit):
	GPIO.setup(blankingPins[digit], GPIO.HIGH)
	return



def countTest():
	blankAll()
	for digit in range(0,6):
		for i in range(0,10):
			setDigit(digit,i)
			unblankDigit(digit)
			time.sleep(.05)
			blankDigit(digit)


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

def scan(interations):
	blankAll()
	for i in range(0,interations):
		print(i)
		for digit in range(0,6):

			setDigit(digit,0)
			unblankDigit(digit)
			time.sleep(.014)
			blankDigit(digit)

def updateTime():
	blankAll()
	time.sleep(.0007)
	now=datetime.datetime.now()
	hour=now.strftime("%H")
	minute=now.strftime("%M")
	second=now.strftime("%S")

	hours=[int(d) for d in str(hour)]
	minutes=[int(x) for x in str(minute)]
	seconds=[int(y) for y in str(second)]

	setDigit(0,hours[0])
	setDigit(1,hours[1])
	setDigit(2,minutes[0])
	setDigit(3,minutes[1])
	setDigit(4,seconds[0])
	setDigit(5,seconds[1])
	unblankAll()
	time.sleep(.0025)

blankAll()
scan(5)
countTest()

while True:
	updateTime()
	#pass
	# time.sleep(5)
	# GPIO.output(35, GPIO.LOW) #Blank digit 2
	# time.sleep(1.5)
	# GPIO.output(35, GPIO.HIGH) #unblank digit 2
	#blinkPin(int(val))
	#time.sleep(2)
	#pass
	#count()
