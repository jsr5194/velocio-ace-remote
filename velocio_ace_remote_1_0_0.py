import sys
import time
import serial


###
### 1. function definitions
###

def print_help():
	print ""
	print "********************************************************************************"
	print "*                                                                              *"
	print "*                             velocio_ace_remote.py                            *"
	print "*                                  version 1.0                                 *"  
	print "*                                                                              *"
	print "********************************************************************************"
	print ""
	print " Usage: python velocio_ace_remote.py [instruction]"
	print ""
	print " Instructions:"
	print " \tplay \t\tstart the routine at current position"
	print " \tpause\t\tpause the routine at current position"
	print " \treset\t\treset the routine to the beginning"
	print ""
	print " Example:  python velocio_ace_remote.py play"
	print ""
	print ""
	exit(1)


# sends a set of instructions to the connected device
# @param instruction_set : an array of commands to send to the PLC in hex
# @param printstring     : runtime message for the user
def send_instruction(instruction_set, printstring):
	print "[*] sending %s instruction ..." % printstring
	for instruction in instruction_set:
		ser.write(instruction)
		time.sleep(0.1)
	print "[*] instruction sent"


###
### 2. handle input errors
###

if len(sys.argv) != 2:
	print_help()

param = sys.argv[1]

if param == "-h" or param == "--help":
	print_help()
	

###
### 3. set up usb serial connection
###

# define serial connection
ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

try:
	# initiate the connection
	ser.isOpen()
	

	###
	### 4. instruction definitions
	###

	press_play = [
	"\x56\xff\xff\x00\x07\xf1\x01"
	]

	press_pause = [
	"\x56\xff\xff\x00\x07\xf1\x02"
	]

	press_reset = [
	"\x56\xff\xff\x00\x07\xf1\x06"
	]


	###
	### 5. process the instruction
	###

	if param == "play":
		send_instruction(press_play, param)

	elif param == "pause":
		send_instruction(press_pause, param)

	elif param == "reset":
		send_instruction(press_reset, param)

	else:
		print_help()


	###
	### 6. clean up
	###

	ser.close()

except Exception as e:
		print ""
		print "[!] ERROR"
		print "[!] MSG: %s" % e
		print ""
		exit(1)

