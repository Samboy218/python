#Sam Wehunt 9/19/2015
"""
This script takes a normal .png image, and hides a message inside it
Usage: python Stego2Opt.py -e/-d <target .png file>
	-e for encode (hide)
	-d for decode (retrieve)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The message is taken from the user and a key is chosen from 'key.txt', this key is used to generate a pseudorandom string of numbers
	these numbers are the indicies of the pixels that will have bits stored into them (the bit will either be stored in teh red or blue channel)
	at the end of the binary message, fifteen 1's and a 0 are appended onto the end for the purpose of decoding at a later time
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
to decode, the same key used in the encoding must be used, and the script takes the same psudorandom string of numbers to find the bits
	this process stops when the end of the data is reached, or a string is found containing fifteen 1's followed by a zero (1111111111111110)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The main difference between this and the 'Stego2.py' is that this uses a different mechanism for getting the indicies for retrieval
	the other script is horribly inefficient in this regard, and makes an array of ints with length equal to the length of .png data (which is often in the millions)
	this script removes that, and only grabs the index of the next bit to retrieve, so it is much better
"""
from PIL import Image
import binascii
import optparse

#pre: r, g, and b are ints between 0-255, which of course represent a pixel
#post: returns a string representing the hexadecimal value of the rgb values passed in
def rgb2hex(r, g, b):
	return "#{:02x}{:02x}{:02x}".format(r, g, b)

#pre:  hexcode is a string representing a hexadecimal value between #000000-#FFFFFF (example: '#1e45a3)
#post: returns a tuple of three values (r, g, b), each from 0-255 that represent a pixel
def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))

#pre: message is a string of ascii characters
#post: returns a string of 0's and 1's which represents the message in it's binary form
def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16))
	return binary[2:]
	
#pre: binary is a string of 1's and 0's
#	  this string must be the correct length to be converted into ascii
#post: a string is returned which is the ascii representation of the binary value passed in
def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b' +binary, 2)))
	return message

#pre: length is an integer
#post: an integer array of length(length) is returned
#	   This array contains an increasing, pseudorandom string of numbers
def getDataIndex(length):
	numlist = []
	newNum = 0
	oldNum = 0
	
	for x in range(0, length):
		newNum = getNextIndex(oldNum)
		numlist.append(newNum)	
		oldNum = newNum
	
	return numlist

#pre: number is an integer
#post: an integer is returned, this integer is pseudorandomly larger than number by 1-10
def getNextIndex(number):
	if (number == 0):
		num = processKey('key.txt')
	else:
		num = number
	return 1 + number + (num * 617 + 35) % 9

#pre: filename is a string that is the name of the file where the key is contained
#post: an integer is returned that is generated randomly based on the key
def processKey(filename):
	file = open(filename)
	key = file.read()
	binKey = str2bin(key)
	
	total = 0
	for count in binKey:
		total = total + int(count, 10)
	
	return total % len(key)
	
#pre: hexcode is a string representing a hexadecimal value between #000000-#FFFFFF (example: '#1e45a3)
#	  digit is a single character, either 1 or 0, to be encoded in the hexadecimal value
#post: returns a string equivalent to the one passed in, but with one character changed (the encoded value)
def encode(hexcode, digit):
	hexcode = hexcode[1:]
	if (hexcode[0] in ('0', '1', '2', '3', '4', '5', '6', '7')):
		hex1half = hexcode[0]
		hex2half = hexcode[2:]
		hexcode = hex1half + digit + hex2half
	else:
		hexcode = hexcode[:-1] + digit
	
	hexcode = '#' + hexcode
	return hexcode
	
#pre:  hexcode is a string representing a hexadecimal value between #000000-#FFFFFF (example: '#1e45a3)
#post: the bit encoded into the hexcode string will be retrieved
#	   if hexcode was never encoded by encode, no error will be raised, and this may return something other than 1 or 0
def decode(hexcode):
	hexcode = hexcode[1:]
	if (hexcode[0] in ('0', '1', '2', '3', '4', '5', '6', '7')):
		return hexcode[1]
	else:
		return hexcode[-1]

#pre: filename is a string that is the name of a .png file
#	  message is a string of ascii characters to be hidden inside the .png file
#post: returns a string that describes whether the operation was successful or not
#	   The indicated .png file is slightly altered to hide the message
def hide(filename, message):
	img = Image.open(filename)
	binary = str2bin(message) + '1111111111111110'
	
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()
		
		newdata = []
		digit = 1
		dataindex = 0
		indexlist = getDataIndex(len(binary))
		for item in datas:
			if ( not(digit == len(indexlist) +1) and dataindex == indexlist[digit-1]):
				newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit-1])
				r, g, b = hex2rgb(newpix)
				newdata.append((r, g, b, 255))
				digit += 1
			else:
				newdata.append(item)
			dataindex += 1
		img.putdata(newdata)
		img.save(filename, 'PNG')
		return 'Completed!'
	return 'Incorrect image mode, could not hide'

#pre: filename is a string that is the name of a .png file
#post: if a message was hidden in the file using the same key as the current one, it is returned as a string
#	   if there is no message, or the wrong key is used, this generally returns garbage or an error will be raised by one of the utility functions
def retr(filename):
	filename = filename
	img = Image.open(filename)
	binary = ''
	
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()
		
		digit = 0
		nextdata = getNextIndex(0)
		for item in datas:
			if (digit == nextdata):
				binary = binary + decode(rgb2hex(item[0], item[1], item[2]))
				if (binary[-16:] == '1111111111111110'):
					return bin2str(binary[:-16])
				nextdata = getNextIndex(nextdata)
			digit+=1
		return bin2str(binary)
	return "incorrect Image mode, couldn't retrieve"

#pre: filename is a string that is the name of a .txt file
#post: returns a string of the contents of the .txt file
def getMessage(filename):
	current_file = open(filename)
	current_file.seek(0)
	return current_file.read()
	
def Main():
	parser = optparse.OptionParser('usage %prog -e/-d <target file>')
	parser.add_option('-e', dest='hide', type='string', help='target picture path to hide text')
	parser.add_option('-d', dest='retr', type='string', help='target picture path to retrieve text')
	
	(options, args) = parser.parse_args()
	if (options.hide != None):
		text = getMessage(raw_input("Enter the file name containing the message to encode: "))
		print hide(options.hide, text)
	elif (options.retr != None):
		print retr(options.retr)
	else:
		print parser.usage
		exit(0)
		
if __name__ == '__main__':
	Main()
