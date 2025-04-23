from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os
from datetime import datetime

from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT
	
	SETUP = 0
	PLAY = 1
	PAUSE = 2
	TEARDOWN = 3

	def __init__(self, master, serveraddr, serverport, rtpport, filename):
		"""Initialize the client with server and video details."""
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.handler)
		self.createWidgets()
		self.serverAddr = serveraddr
		self.serverPort = int(serverport)
		self.rtpPort = int(rtpport)
		self.fileName = filename
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.connectToServer()
		self.frameNbr = 0

		 # Statistical Analysis Variables
		self.outOfRuntime = False
		self.firstPacket = False
		self.totalJitter = 0
		self.startTime = datetime.now()
		self.playTime = datetime.now() - datetime.now()
		self.packetsLost = 0
		self.packetLossRate = 0.0
		self.totalPacketsReceived = 0
		self.videoDataRate = 0
		self.numberOfBytesReceived = 0

		self.arrivalTimeOfPacket = 0.0
		self.arrivalTimeOfPreviousPacket = 0.0
		self.interPacketSpacing = 0.0
		self.previousInterPacketSpacing = 0.0

	def createWidgets(self):
		"""Build the GUI for the client."""
		# Create Setup button
		self.setup = Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		# Create Play button		
		self.start = Button(self.master, width=20, padx=3, pady=3)
		self.start["text"] = "Play"
		self.start["command"] = self.playMovie
		self.start.grid(row=1, column=1, padx=2, pady=2)
		
		# Create Pause button			
		self.pause = Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)
		
		# Create Teardown button
		self.teardown = Button(self.master, width=20, padx=3, pady=3)
		self.teardown["text"] = "Teardown"
		self.teardown["command"] =  self.exitClient
		self.teardown.grid(row=1, column=3, padx=2, pady=2)
		
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5) 
	
	def setupMovie(self):
		"""Handle the Setup button click."""
		if self.state == self.INIT:
			self.sendRtspRequest(self.SETUP)
	
	def exitClient(self):
		"""Handle the Teardown button click."""
		self.sendRtspRequest(self.TEARDOWN)		
		self.master.destroy() # Close the gui window
		os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT) # Delete the cache image from video

	def pauseMovie(self):
		"""Handle the Pause button click."""
		if self.state == self.PLAYING:
			self.sendRtspRequest(self.PAUSE)
	
	def playMovie(self):
		"""Handle the Play button click."""
		if self.state == self.READY:
			# Create a new thread to listen for RTP packets
			threading.Thread(target=self.listenRtp).start()
			self.playEvent = threading.Event()
			self.playEvent.clear()
			self.sendRtspRequest(self.PLAY)
	
	def listenRtp(self):		
		"""Listen for RTP packets from the server."""
		while True:
			try:
				data = self.rtpSocket.recv(20480)
				if data:
					rtpPacket = RtpPacket()
					rtpPacket.decode(data)

					currFrameNbr = rtpPacket.seqNum()
					print("Current Seq Num: " + str(currFrameNbr))

					# Jitter Calculation
					if not self.outOfRuntime:
						if currFrameNbr > 500:
							self.outOfRuntime = True
							self.playTime += datetime.now() - self.startTime
							break
					else:
						break

					self.totalPacketsReceived += 1  # packet received increment total
					self.numberOfBytesReceived += sys.getsizeof(rtpPacket.getPacket())

					if self.frameNbr+1 >= currFrameNbr and not self.firstPacket:  # calculation is valid (Not following a lost packet)
						self.arrivalTimeOfPreviousPacket = self.arrivalTimeOfPacket
						self.arrivalTimeOfPacket = datetime.now().second + datetime.now().microsecond/1000000  # Arrival time

						self.previousInterPacketSpacing = self.interPacketSpacing
						self.interPacketSpacing = self.arrivalTimeOfPacket - self.arrivalTimeOfPreviousPacket
						jitterIncrement = abs(self.interPacketSpacing - self.previousInterPacketSpacing)
						self.totalJitter = self.totalJitter + jitterIncrement
					elif self.firstPacket:
						self.firstPacket = False
						self.arrivalTimeOfPacket = datetime.now().second + datetime.now().microsecond/1000000  # Arrival time
						self.interPacketSpacing = 0
					else:  # There was a packet loss
						self.arrivalTimeOfPacket = datetime.now().second + datetime.now().microsecond/1000000  # Arrival time
						self.interPacketSpacing = 0
						self.packetsLost += currFrameNbr - self.frameNbr - 1  # increment for packet loss

					if currFrameNbr > self.frameNbr: # Discard the late packet
						self.frameNbr = currFrameNbr
						self.updateMovie(self.writeFrame(rtpPacket.getPayload()))

			except:
				# Stop listening upon requesting PAUSE or TEARDOWN
				if self.playEvent.isSet(): 
					break
				
				# Upon receiving ACK for TEARDOWN request,
				# close the RTP socket
				if self.teardownAcked == 1:
					self.rtpSocket.shutdown(socket.SHUT_RDWR)
					self.rtpSocket.close()
					break
					
	def writeFrame(self, data):
		"""Write the received frame to a temporary image file."""
		cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		file = open(cachename, "wb")
		file.write(data)
		file.close()
		
		return cachename
	
	def updateMovie(self, imageFile):
		"""Update the GUI with the new video frame."""
		photo = ImageTk.PhotoImage(Image.open(imageFile))
		self.label.configure(image = photo, height=288) 
		self.label.image = photo
		
	def connectToServer(self):
		"""Connect to the RTSP server."""
		self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.rtspSocket.connect((self.serverAddr, self.serverPort))
		except:
			tkinter.messagebox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
		
		print ("Connected to server\n")
	
	def sendRtspRequest(self, requestCode):
		"""Send an RTSP request to the server."""
		VERSION = "RTSP/1.0"

		# Setup request
		if requestCode == self.SETUP and self.state == self.INIT:
			threading.Thread(target=self.recvRtspReply).start()
			self.rtspSeq += 1
			request = "SETUP %s %s\n" % (self.fileName, VERSION)
			request+="CSeq: %d\n" % self.rtspSeq
			request+="Transport: RTP/UDP; client_port= %d" % (self.rtpPort)
			self.requestSent = self.SETUP
		
		# Play request
		elif requestCode == self.PLAY and self.state == self.READY:
			self.rtspSeq += 1
			request = "PLAY %s %s\n" % (self.fileName, VERSION)
			request += "CSeq: %d\n" % self.rtspSeq
			request += "Session: %d" % self.sessionId
			self.requestSent = self.PLAY
		
		# Pause request
		elif requestCode == self.PAUSE and self.state == self.PLAYING:
			self.rtspSeq += 1
			request = "PAUSE %s %s\n" % (self.fileName, VERSION)
			request += "CSeq: %d\n" % self.rtspSeq
			request += "Session: %d" % self.sessionId
			self.requestSent = self.PAUSE
			
		# Teardown request
		elif requestCode == self.TEARDOWN and not self.state == self.INIT:
			self.rtspSeq += 1
			request = "TEARDOWN %s %s\n" % (self.fileName, VERSION)
			request += "CSeq: %d\n" % self.rtspSeq
			request += "Session: %d" % self.sessionId
			self.requestSent = self.TEARDOWN
			
		else:
			return
		
		self.rtspSocket.sendall(request.encode('utf-8'))
		print('\nClient:\n' + request)
	
	def recvRtspReply(self):
		"""Receive and process RTSP replies from the server."""
		while True:
			reply = self.rtspSocket.recv(1024)
			
			if reply:
				self.parseRtspReply(reply)

			if not self.outOfRuntime and (self.requestSent == self.PAUSE or self.state == self.INIT and self.requestSent == self.TEARDOWN):
				self.playTime += datetime.now() - self.startTime
			elif self.requestSent == self.PLAY:
				self.startTime = datetime.now()
				self.firstPacket = True

			if self.requestSent == self.TEARDOWN:
				self.rtspSocket.shutdown(socket.SHUT_RDWR)
				self.rtspSocket.close()

				if self.totalPacketsReceived > 0:
					print("\nNumber of Lost Packets: " + str(self.packetsLost))
					print("Number of Packets Received: " + str(self.totalPacketsReceived))
					self.packetLossRate = self.packetsLost / (self.totalPacketsReceived + self.packetsLost)
					print("Packet loss rate: " + str(self.packetLossRate))
					print("Number of Bytes Received: " + str(self.numberOfBytesReceived))
					print("playTime: " + str(self.playTime.seconds + self.playTime.microseconds/1000000))
					self.videoDataRate = self.numberOfBytesReceived / (self.playTime.seconds + self.playTime.microseconds/1000000)
					print("Video data rate: " + str(self.videoDataRate) + " bytes/second")
					print("TotalJitter: " + str(self.totalJitter))
					self.averageJitter = self.totalJitter / self.totalPacketsReceived
					print("AverageJitter: " + str(self.averageJitter))
				else:
					print("\nNumber of Lost Packets: " + str(self.packetsLost))
					print("Number of Packets Received: " + str(self.totalPacketsReceived))
					print("Packet loss rate: " + str(self.packetLossRate))
					print("Number of Bytes Received: " + str(self.numberOfBytesReceived))
					print("playTime: 0")
					self.videoDataRate = 0
					print("Video data rate: " + str(self.videoDataRate) + " bytes/second")
					print("TotalJitter: " + str(self.totalJitter))
					self.averageJitter = 0
					print("AverageJitter: " + str(self.averageJitter))
				break
	
	def parseRtspReply(self, data):
		"""Parse the RTSP reply from the server."""
		decodedData = data.decode()
		lines = decodedData.split('\n')
		seqNum = int(lines[1].split(' ')[1])
		
		print ("\nServer:\n" + decodedData)
		
		if seqNum == self.rtspSeq:
			session = int(lines[2].split(' ')[1])
			if self.sessionId == 0:
				self.sessionId = session
			
			if self.sessionId == session:
				if int(lines[0].split(' ')[1]) == 200: 
					if self.requestSent == self.SETUP:
						self.state = self.READY
						self.openRtpPort()
					elif self.requestSent == self.PLAY:
						self.state = self.PLAYING
					elif self.requestSent == self.PAUSE:
						self.state = self.READY
						self.playEvent.set()
					elif self.requestSent == self.TEARDOWN:
						self.state = self.INIT
						self.teardownAcked = 1 
	
	def openRtpPort(self):
		"""Open the RTP port to receive video data."""
		self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.rtpSocket.settimeout(0.5)
		
		try:
			self.state = self.READY
			self.rtpSocket.bind(('', self.rtpPort))
		except:
			tkinter.messagebox.showwarning('Unable to Bind', 'Unable to bind PORT=%d' %self.rtpPort)

	def handler(self):
		"""Handle the GUI window close event."""
		self.pauseMovie()
		if tkinter.messagebox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.exitClient()
		else:
			self.playMovie()