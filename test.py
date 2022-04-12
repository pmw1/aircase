import time
import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c=busio.I2C(board.SCL, board.SDA)
time.sleep(1)
mcp=MCP23017(i2c, address=0x20)


pin0=mcp.get_pin(0)
pin1=mcp.get_pin(1)
pin0.direction=Direction.OUTPUT
pin1.direction=Direction.OUTPUT

while True:
    pin1.value=True
    pin0.value=False
    time.sleep(.005)
    pin1.value=False
    pin0.value=True
    time.sleep(.005)



