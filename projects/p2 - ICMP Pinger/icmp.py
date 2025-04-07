from socket import *  # Import all functions and constants from the socket module
import os  # Provides functions for interacting with the operating system
import sys  # Provides access to system-specific parameters and functions
import struct  # Used for working with C-style data structures
import time  # Provides time-related functions
import select  # Provides I/O multiplexing
import binascii  # Provides functions for binary and ASCII conversions

# ICMP message type for Echo Request (used for ping)
ICMP_ECHO_REQUEST = 8

# Function to calculate the checksum of a packet
def checksum(data): 
    csum = 0
    countTo = (len(data) // 2) * 2  # Process data in 16-bit chunks
    count = 0

    # Sum up 16-bit chunks
    while count < countTo:
        thisVal = data[count + 1] * 256 + data[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff  # Keep checksum within 32 bits
        count = count + 2

    # Add any remaining byte (if data length is odd)
    if countTo < len(data):
        csum = csum + data[-1]
        csum = csum & 0xffffffff

    # Fold 32-bit checksum to 16 bits
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum  # Take the one's complement
    answer = answer & 0xffff  # Mask to 16 bits
    answer = answer >> 8 | (answer << 8 & 0xff00)  # Swap bytes for network order
    return answer

# Function to receive a single ping reply
def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout  # Time left to wait for a reply

    while True: 
        startedSelect = time.time()  # Record the time before select
        # Wait for the socket to become readable or timeout
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)  # Time spent in select
        if whatReady[0] == []:  # Timeout occurred
            return "Request timed out."

        timeReceived = time.time()  # Record the time the packet was received
        recPacket, addr = mySocket.recvfrom(1024)  # Receive the packet

        # Extract the ICMP header from the received packet
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

        # Check if the packet ID matches the one we sent
        if packetID == ID:
            bytesInDouble = struct.calcsize("d")  # Size of the timestamp in the packet
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]  # Extract the timestamp
            ttl = struct.unpack("B", recPacket[8:9])[0]  # Extract TTL from the IP header
            rtt = (timeReceived - timeSent) * 1000  # Calculate round-trip time in milliseconds
            return f"{len(recPacket)} bytes from {destAddr}: time={rtt:.3f} ms TTL={ttl}"

        # Update the remaining time to wait
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:  # Timeout occurred
            return "Request timed out."

# Function to send a single ping request
def sendOnePing(mySocket, destAddr, ID):
    # Create a dummy ICMP header with a checksum of 0
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())  # Add the current timestamp as data

    # Calculate the checksum for the header and data
    myChecksum = checksum(header + data)

    # Convert checksum to network byte order
    if sys.platform == 'darwin':  # Special handling for macOS
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    # Recreate the header with the correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data  # Combine header and data into a single packet

    # Send the packet to the destination address
    mySocket.sendto(packet, (destAddr, 1))

# Function to perform a single ping operation
def doOnePing(destAddr, timeout): 
    icmp = getprotobyname("icmp")  # Get the protocol number for ICMP
    mySocket = socket(AF_INET, SOCK_RAW, icmp)  # Create a raw socket

    myID = os.getpid() & 0xFFFF  # Use the process ID as the packet ID
    sendOnePing(mySocket, destAddr, myID)  # Send the ping request
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)  # Wait for the reply

    mySocket.close()  # Close the socket
    return delay

# Function to continuously ping a host
def ping(host, timeout=1):
    dest = gethostbyname(host)  # Resolve the hostname to an IP address
    print(f"Pinging {dest} using Python:")
    print("")

    while True:
        delay = doOnePing(dest, timeout)  # Perform a single ping
        print(delay)  # Print the result
        time.sleep(1)  # Wait for 1 second before sending the next ping

# Start pinging google.com
ping("google.com")