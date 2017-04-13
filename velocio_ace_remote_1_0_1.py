import sys
import time
import serial

# define serial connection
ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

def print_help():
	print ""
	print "********************************************************************************"
	print "*                                                                              *"
	print "*                             velocio_ace_remote.py                            *"
	print "*                                 version 1.0.1                                *"  
	print "*                                                                              *"
	print "********************************************************************************"
	print ""
	print " Usage: python velocio_ace_remote.py [instruction]"
	print ""
	print " Control Instructions:"
	print " \tplay \t\t\tstart the routine at current position"
	print " \tpause\t\t\tpause the routine at current position"
	print " \treset\t\t\treset the routine to the beginning"
	print " \tset_output_1_off\tset output 1 to off"
	print " \tset_output_2_off\tset output 2 to off"
	print " \tset_output_3_off\tset output 3 to off"
	print " \tset_output_4_off\tset output 4 to off"
	print " \tset_output_5_off\tset output 5 to off"
	print " \tset_output_6_off\tset output 6 to off"
	print " \tset_output_1_on\t\tset output 1 to on"
	print " \tset_output_2_on\t\tset output 2 to on"
	print " \tset_output_3_on\t\tset output 3 to on"
	print " \tset_output_4_on\t\tset output 4 to on"
	print " \tset_output_5_on\t\tset output 5 to on"
	print " \tset_output_6_on\t\tset output 6 to on"
	print ""
	print ""
	print " Read Instructions:"
	print ""
	print " \tread_input_bits\t\tquery the input bits and print the response"
	print " \tread_output_bits\tquery the output bits and print the response"
	print ""
	print ""
	print " Debug Instructions:"
	print ""
	print " \tenter_debug\t\tput the device into debug mode for testing"
	print " \texit_debug\t\texit the device debug mode for normal operation"
	print " \tstep_into\t\tstandard procedure"
	print " \tstep_out\t\tstandard procedure"
	print " \tstep_over\t\tstandard procedure"
	print ""
	print ""
	print " Example:\tpython velocio_ace_remote.py play"
	print " Example:\tpython velocio_ace_remote.py read_output_bits"
	print " Example:\tpython velocio_ace_remote.py exit_debug"
	print ""
	print ""
	exit(1)


# sends a set of instructions to the connected device
# @param instruction_set : an array of commands to send to the PLC in hex
# @param printstring     : runtime message for the user
def send_instruction(instruction_set, printstring):
	# clear out any leftover data
	if ser.inWaiting() > 0: 
		ser.flushInput()

	print "[*] sending %s instruction ..." % printstring

    # perform the write
	for instruction in instruction_set:
		ser.write(instruction)
		time.sleep(0.1)

		# handle printout for any read requests
		if "read" in printstring:
			cur_reg = instruction[-1:].encode('hex')
			response = ""
			while ser.inWaiting() > 0:
				response += "\\x%s" % ser.read().encode('hex')
			time.sleep(0.1)
			
			response = response.replace("\\x", "").strip()
			ascii_response = ""
			for letter in response.decode('hex'):
				charcode = ord(letter)
				if ((charcode < 123 and charcode > 64) or (charcode > 47 and charcode < 58)):
					ascii_response += letter
				else:
					ascii_response += "_"
			output_header = "\\x%s:\t" % cur_reg
			output_footer = "\t%s" % ascii_response
			
			print "%s%s%s" % (output_header, response, output_footer)
		else:
			print "[*] instruction sent"


def main():
	# handle input errors
	if len(sys.argv) != 2: 
		print_help()

	# get cmd line arg
	param = sys.argv[1]

	# check for help request
	if param == "-h" or param == "--help": 
		print_help()

	# initiate the connection
	ser.isOpen()
	

	###
	# process the instruction
	###

	# control
	if param == "play": send_instruction(press_play, param)
	elif param == "pause": send_instruction(press_pause, param)
	elif param == "reset": send_instruction(press_reset, param)
	elif param == "step_into": send_instruction(step_into, param)
	elif param == "step_out": send_instruction(step_out, param)
	elif param == "step_over": send_instruction(step_over, param)
	elif param == "enter_debug": send_instruction(enter_debug, param)
	elif param == "exit_debug": send_instruction(exit_debug, param)
	elif param == "set_output_1_off": send_instruction(set_output_1_off, param)
	elif param == "set_output_1_on": send_instruction(set_output_1_on, param)
	elif param == "set_output_2_off": send_instruction(set_output_2_off, param)
	elif param == "set_output_2_on": send_instruction(set_output_2_on, param)
	elif param == "set_output_3_off": send_instruction(set_output_3_off, param)
	elif param == "set_output_3_on": send_instruction(set_output_3_on, param)
	elif param == "set_output_4_off": send_instruction(set_output_4_off, param)
	elif param == "set_output_4_on": send_instruction(set_output_4_on, param)
	elif param == "set_output_5_off": send_instruction(set_output_5_off, param)
	elif param == "set_output_5_on": send_instruction(set_output_5_on, param)
	elif param == "set_output_6_off": send_instruction(set_output_6_off, param)
	elif param == "set_output_6_on": send_instruction(set_output_6_on, param)

	# read
	elif param == "read_input_bits": send_instruction(read_input_bits, param)
	elif param == "read_output_bits": send_instruction(read_output_bits, param)

	# edge cases
	else: print_help()

	# clean up
	ser.close()



if __name__ == "__main__":

	###
	# define the instructions
	###

	# control instructions
	press_play =       ["\x56\xff\xff\x00\x07\xf1\x01"]
	press_pause =      ["\x56\xff\xff\x00\x07\xf1\x02"]
	press_reset =      ["\x56\xff\xff\x00\x07\xf1\x06"]
	step_into =        ["\x56\xff\xff\x00\x07\xf1\x03"]
	step_out =         ["\x56\xff\xff\x00\x07\xf1\x04"]
	step_over =        ["\x56\xff\xff\x00\x07\xf1\x05"]
	enter_debug =      ["\x56\xff\xff\x00\x07\xf0\x02"]
	exit_debug =       ["\x56\xff\xff\x00\x07\xf0\x01"]
	set_output_1_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x01\x00\x00\x00"]
	set_output_2_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x02\x00\x00\x00"]
	set_output_3_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x04\x00\x00\x00"]
	set_output_4_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x08\x00\x00\x00"]
	set_output_5_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x10\x00\x00\x00"]
	set_output_6_off = ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x20\x00\x00\x00"]
	set_output_1_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x01\x00\x00\x01"]
	set_output_2_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x02\x00\x00\x01"]
	set_output_3_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x04\x00\x00\x01"]
	set_output_4_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x08\x00\x00\x01"]
	set_output_5_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x10\x00\x00\x01"]
	set_output_6_on =  ["\x56\xff\xff\x00\x15\x11\x01\x00\x01\x00\x00\x09\x01\x00\x00\x01\x00\x20\x00\x00\x01"]


	# read instructions
	read_input_bits = [
	"\x56\xff\xff\x00\x08\x0a\x00\x01",
	"\x56\xff\xff\x00\x08\x0a\x00\x02",
	"\x56\xff\xff\x00\x08\x0a\x00\x03",
	"\x56\xff\xff\x00\x08\x0a\x00\x04",
	"\x56\xff\xff\x00\x08\x0a\x00\x05",
	"\x56\xff\xff\x00\x08\x0a\x00\x06"
	]

	read_output_bits = [
	"\x56\xff\xff\x00\x08\x0a\x00\x07",
	"\x56\xff\xff\x00\x08\x0a\x00\x08",
	"\x56\xff\xff\x00\x08\x0a\x00\x09",
	"\x56\xff\xff\x00\x08\x0a\x00\x0a",
	"\x56\xff\xff\x00\x08\x0a\x00\x0b",
	"\x56\xff\xff\x00\x08\x0a\x00\x0c"
	]


	try:
		print ""
		main()
		print ""

	except Exception as e:
		print ""
		print "[!] ERROR"
		print "[!] MSG: %s" % e
		print ""
		exit(1)

