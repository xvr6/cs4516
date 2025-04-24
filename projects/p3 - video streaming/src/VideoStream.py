class VideoStream:
	def __init__(self, filename):
		"""Initialize the VideoStream with the given filename."""
		self.filename = filename
		try:
			self.file = open(filename, 'rb')  # Open the video file in binary read mode
		except FileNotFoundError:
			raise IOError(f"File {filename} not found.")  # Raise an error if the file cannot be opened
		self.frameNum = 0  # Initialize the frame number
		
	def nextFrame(self):
		"""Read and return the next frame from the video file."""
		data = self.file.read(5)  # Read the frame length from the first 5 bytes
		if data: 
			framelength = int(data)  # Convert the frame length to an integer
							
			# Read the current frame based on the frame length
			data = self.file.read(framelength)
			self.frameNum += 1  # Increment the frame number
		return data  # Return the frame data
		
	def frameNbr(self):
		"""Return the current frame number."""
		return self.frameNum

