from socket import *
import os
import sys
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8

def checksum(str): 
	csum = 0
	countTo = (len(str) / 2) * 2
	
	count = 0
	while count < countTo:
		thisVal = ord(str[count+1:count+2]) * 256 + ord(str[count:count+1])
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(str):
		csum = csum + ord(str[-1])
		csum = csum & 0xffffffff
	
	#Fill in start
	#add the upper 16 bits with the lower 16bits of csum;
	#add the carry-over bit back to lower bits of csum;
	#flip everybit of csum and put it into variable "answer"
      	#Fill in end
	
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer 
	
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
	
	while 1: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out."
		
		#Fill in start
		# get the time the packet is received and store it in "timeReceived"
		# receive the packet from socket and extract information into "recPacket, addr"
        		# fetch the ICMP header from the IP packet
		# get TTL, icmpType, code, checksum, packetID, and sequence
		# get data payload, and return information that can be print later, including byte_data, time used from packet sent to received, TTL
      		#Fill in end
				
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out."
	
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	
	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	
	#Fill in start   
	# Use current time as data payload and put it into "data" variable
	# Calculate the checksum on the data and the dummy header and put it into "myChecksum" variable
	#Fill in end
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
		
	#Fill in start   
	# update the header with correct checksum
	# create a variable "packet" that combines the header and the data payload
	#Fill in end
		
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")
	
	#Fill in start   
	# create a socket with SOCK_RAW as the socket type, and icmp as the protocol; 
	# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
	#Fill in end
	
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay
	
def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	#print "Pinging " + dest + " using Python:"
	print("")

	#print ""
	# Send ping requests to a server separated by approximately one second
	while 1 :
		delay = doOnePing(dest, timeout)
		print(delay)
		time.sleep(1)# one second
	return delay
	
ping("google.com")

