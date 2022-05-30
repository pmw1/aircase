import smbus
import time
import os
 

bus = smbus.SMBus(1) # Rev 2 Pi uses 1  #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0

ICaddr=[0x20,0x22,0x24] # list variable of ic device addresses 

IODIRA1 = 0x00 # Pin direction register GPA
IODIRB1 = 0x01 # Pin direction register GPB

GPIOA1 = 0x12 # Register for inputs GPA
GPIOB1 = 0x13 # Register for inputs GPB

OLATA1  = 0x14 # Register for outputs for GPA
OLATB1  = 0x15 # Register for outputs for GPB

ledStatus=[0,0,0,0] ## Status codes ic0/GPIOA, ic0/GPIOB, ic1/GPIOA, ic1/GPIOB
inputStatus=[0,0]

indList={} ## declare dictionary for indicator loactions
inputs={} ## delcare dictionary for input locations

def clearIC(ic):## Clear defined IC
	print("Clearing IC: {}".format(ic))
	bus.write_byte_data(ICaddr[ic],IODIRA1,0x00) #Set all GPA pins as outputs by setting all bits of IODIRA register to 0
	bus.write_byte_data(ICaddr[ic],IODIRB1,0x00) #Set all GPA pins as outputs by setting all bits of IODIRA register to 0
	bus.write_byte_data(ICaddr[ic],OLATA1,0) # Set output all 7 output bits to 0
	bus.write_byte_data(ICaddr[ic],OLATB1,0) # Set output all 7 output bits to 0


def initialize(): ## clear ICs 
	for i in range(0,2):
		clearIC(i)

	bus.write_byte_data(ICaddr[2],OLATA1,0xFF) ## set ic2 to all pins as input
	bus.write_byte_data(ICaddr[2],OLATB1,0xFF) ## set ic2 to all pins as input

def manualEnter():
  number = input('enter a number: ')
  if number=="clear":
  	clearIC(1)
  	return
  integer=int(number)
  STATUS1[0]=integer
  binary=format(STATUS1[0], "08b")
  hexcode=format(STATUS1[0], "X")
  display=binary[::-1]
  decimal=format(STATUS1[0], "d")

  print('Binary :  {}'.format(binary))
  print('Hex    :  {}'.format(hexcode))
  print('Display:  {}'.format(display))

  bus.write_byte_data(ICaddr[0],OLATA1,STATUS1[0]) ##write code to bank1

def defineIndicatorList(): #chip,bank,bitposition 0-7
	indList['atomic']=[0,"GPB",0]
	indList['warning']=[0,"GPA",1]
	indList['netTestRunning']=[0,"GPA",2]
	indList['pcPower']=[1,"GPA",4]

def defineInputs(): #chip, bank, bit position 0-7,lock (0=open/1=locked)
	inputs['runPing']=[2,"GPA",0,0]
	inputs['runBandwidth']=[2,"GPB",1,0]

def turnONref():
	startCode=STATUS1[0]
	startBinary=format(STATUS1[0], "08b")
	print("start code    :  {}".format(startCode))
	print("start binary  :  {}".format(startBinary))
	print("---------")
	endCode=STATUS1[0] & ~ (1<<2)
	endBinary=format(endCode, "08b")
	print("end code      :  {}".format(endCode))
	print("end binary    :  {}".format(endBinary))

def turnOnLED(ledName):
	#print("\n--Turning on LED--")
	ic=indList[ledName][0] ##make local variable for ic number
	gp=format(indList[ledName][1])  ## make local variable for side of IC chip (GPA or GPB)
	pin=indList[ledName][2] ##  make local vaiable fro pin position
	#print("LED: {}".format(ledName))
	#print("IC: {}".format(ic))
	#print("GP: {}".format(gp))
	#print("PIN: {}".format(pin))

	if ic == 0 and gp == "GPA":  ## if ic0 & GPA
		ledStatus[0]=ledStatus[0]|(1<<pin)
	if ic == 0 and gp == "GPB":  ## if ic0 & GPB
		ledStatus[1]=ledStatus[1]|(1<<pin)
	if ic == 1 and gp == "GPA": ## if ic1 & GPA
		ledStatus[2]=ledStatus[2]|(1<<pin)
	if ic == 1 and gp == "GPB": ## if ic1 # GPB
		ledStatus[3]=ledStatus[3]|(1<<pin)

	updateLeds()
	return True
	
	#if(indList[ledName][0]==0) and (indList[ledName][1]==0)
	#print("Turning on: {}, Chip {}, Bank {}, Bit Position {}".format(ledName, indList[ledName][0], indList[ledName][1],indList[ledName][2]))
	#print("Changing from {}  -  {}".format(STATUS1[0]),"08b")
	#binary=format(STATUS1[0], "08b")
	#STATUS1[0]=STATUS1[0]|(1<<indList[ledName][2])
	#print("Changed to: {}".format(STATUS1[0], "08b"))

def turnOffLED(ledName):
	#print("\n--Turning off LED--")
	ic=indList[ledName][0] ##make local variable for ic number
	gp=format(indList[ledName][1])  ## make local variable for side of IC chip (GPA or GPB)
	pin=indList[ledName][2] ##  make local vaiable fro pin position
	#print("LED: {}".format(ledName))
	#print("IC: {}".format(ic))
	#print("GP: {}".format(gp))
	#print("PIN: {}".format(pin))

	if ic == 0 and gp == "GPA":  ## if ic0 & GPA
		ledStatus[0]=ledStatus[0] & ~ (1<<pin)
	if ic == 0 and gp == "GPB":  ## if ic0 & GPB
		ledStatus[1]=ledStatus[1] & ~ (1<<pin)
	if ic == 1 and gp == "GPA": ## if ic1 & GPA
		ledStatus[2]=ledStatus[2] & ~ (1<<pin)
	if ic == 1 and gp == "GPB": ## if ic1 # GPB
		ledStatus[3]=ledStatus[3] & ~ (1<<pin)
		
	updateLeds()
	return True

def updateLeds():

	bus.write_byte_data(ICaddr[0],OLATA1,ledStatus[0]) ##write code to bank1
	bus.write_byte_data(ICaddr[0],OLATB1,ledStatus[1]) ##write code to bank1

	bus.write_byte_data(ICaddr[1],OLATA1,ledStatus[2]) ##write code to bank1
	bus.write_byte_data(ICaddr[1],OLATB1,ledStatus[3]) ##write code to bank1

	####chip commented out because its not currently being used for LED disply.
	#### This chip should be used as input
	
	#bus.write_byte_data(ICaddr[2],OLATA1,ledStatus[0]) ##write code to bank1
	#bus.write_byte_data(ICaddr[2],OLATB1,ledStatus[0]) ##write code to bank1
	#print("updating leds")

def pollInputs(ic,bank):
	if bank == "GPA":
		hexcode = bus.read_byte_data(ICaddr[ic],GPIOA1)
		inputStatus[0]=hexcode
	if bank == "GPB":
		hexcode = bus.read_byte_data(ICaddr[ic],GPIOB1)
		inputStatus[1]=hexcode
	#print(hexcode)





def buttonPressGeneric():
	####ON PRESS
	if inputs['runPing'][3]==0:
		if not (checkBit(inputStatus[0],2)):
			turnOnLED("netTestRunning")
			inputs['runPing'][3]=1 ##lock button

	####ON RELEASE
	if inputs["runPing"][3]==1: ##if lock is enabled
		if(checkBit(inputStatus[0],2)): ## if input bit is 1 (not pressed)
			print("BUTTON OPEN")
			turnOffLED("netTestRunning")
			inputs['runPing'][3]=0 ##unlock button
			blink("netTestRunning",10)
			ip="192.168.140.101"
			response = os.system("ping -c 1 -a " + ip)
			print(response)
			if response == 0:
				print("Network Active")



#--------
def testCount(time):
	for bit in range(0,1000):
		bus.write_byte_data(ICaddr[0],OLATA1,bit) ##write code to bank1
		bus.write_byte_data(ICaddr[0],OLATB1,bit) ##write code to bank1
		time.sleep(.01)
		clearIC(i)
	return

def testAllLedOn():
	for bank in range(0,4):
		for pin in range(0,8):
			ledStatus[bank]=ledStatus[bank]|(1<<pin)
	updateLeds()

def testAllLedOff():
	for bank in range(0,4):
		for pin in range(0,8):
			ledStatus[bank]=ledStatus[bank] & ~ (1<<pin)
	updateLeds()

def test1(ic):
	bus.write_byte_data(ICaddr[ic],OLATA1,48) # Set output all 7 output bits to 0
	bus.write_byte_data(ICaddr[ic],OLATB1,324) # Set output all 7 output bits to 0
	updateLeds()

def test2():
	turnOnLED("warning")
	turnOnLED("atomic")
	turnOnLED("netTestRunning")
	turnOnLED("pcPower")
	time.sleep(3)
	turnOffLED("warning")
	turnOffLED("atomic")
	turnOffLED("netTestRunning")
	turnOffLED("pcPower")

def blink(ledName,numBlinks):
	for i in range(1,numBlinks):
		turnOnLED(ledName)
		time.sleep(.04)
		turnOffLED(ledName)
		time.sleep(.04)



def checkBit(hexcode,bitPosition):
	if (hexcode & (1<<bitPosition)):
		#print(hexcode)
		return True
	else:
		return False


initialize()
defineIndicatorList()
defineInputs()



#blink("atomic",100)
while True:
	 #MySwitch = bus.read_byte_data(ICaddr[2],GPIOA1)
	 #MySwitch=format(MySwitch, "08b")
	 #print(MySwitch)
	 
	 pollInputs(2,"GPA")
	 pollInputs(2,"GPB")

	 #print("input status A: "+str(inputStatus[0]))
	 #print("input status B: "+str(inputStatus[1]))


	 buttonPressGeneric()





	 #time.sleep(.3)
	# testAllLedOn()
	# time.sleep(2)
	# testAllLedOff()
	# time.sleep(2)

#	pass
 
# Set all bits to zero
#bus.write_byte_data(ICaddr[0],OLATA1,0)