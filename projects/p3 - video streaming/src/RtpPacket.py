from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		"""Initialize an empty RTP packet."""
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		        
		# Encode the first byte of the header
		# Version: 2 bits, Padding: 1 bit, Extension: 1 bit, CC: 4 bits
		header[0] = (header[0] | version << 6) & 0xC0  # 1100 0000
		header[0] = (header[0] | padding << 5) & 0x20  # 0010 0000
		header[0] = (header[0] | extension << 4) & 0x10  # 0001 0000
		header[0] = (header[0] | cc) & 0x0F  # 0000 1111
		
		# Encode the second byte of the header
		# Marker: 1 bit, Payload Type: 7 bits
		header[1] = (header[1] | marker << 7) & 0x80  # 1000 0000
		header[1] = (header[1] | pt) & 0x7F  # 0111 1111
		
		# Encode the sequence number (16 bits)
		header[2] = (seqnum & 0xFF00) >> 8  # First 8 bits
		header[3] = (seqnum & 0x00FF)  # Second 8 bits
		
		# Encode the timestamp (32 bits)
		header[4] = (timestamp >> 24)  # First 8 bits
		header[5] = (timestamp >> 16) & 0xFF  # Second 8 bits
		header[6] = (timestamp >> 8) & 0xFF  # Third 8 bits
		header[7] = (timestamp & 0xFF)  # Fourth 8 bits
		
		# Encode the SSRC (32 bits)
		header[8] = (ssrc >> 24)  # First 8 bits
		header[9] = (ssrc >> 16) & 0xFF  # Second 8 bits
		header[10] = (ssrc >> 8) & 0xFF  # Third 8 bits
		header[11] = ssrc & 0xFF  # Fourth 8 bits
		
		# Set the header and payload
		self.header = header
		self.payload = payload
		
	def decode(self, byteStream):
		"""Decode the RTP packet from a byte stream."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload